"""
WebSocket consumer for real-time chat functionality.
Handles connection, message sending, and room management.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket connections for chat rooms.
    Users join a room and can send/receive messages in real-time.
    """

    async def connect(self):
        """
        Called when WebSocket connection is established.
        Joins the user to a chat room group.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Get user from scope (set by AuthMiddleware)
        self.user = self.scope.get('user')

        # Check if user is authenticated
        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept(subprotocol='authorization')

        # Notify others that user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_online',
                'username': self.user.username,
                'action': 'joined'
            }
        )

    async def disconnect(self, close_code):
        """
        Called when WebSocket connection is closed.
        Removes user from the chat room group.
        """
        if hasattr(self, 'room_group_name') and hasattr(self, 'user'):
            # Notify others that user left
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_online',
                    'username': self.user.username,
                    'action': 'left'
                }
            )
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Called when a message is received from WebSocket.
        Saves message to database and broadcasts to room group.
        """
        data = json.loads(text_data)
        message_content = data.get('message', '')

        if not message_content.strip():
            return

        message = await self.save_message(message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': self.user.username,
                'timestamp': message.timestamp.isoformat()
            }
        )

    async def chat_message(self, event):
        """
        Handles chat_message event from group.
        Sends message to WebSocket client.
        """
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

    async def user_online(self, event):
        """
        Handles user online status changes.
        Notifies clients when users join or leave.
        """
        await self.send(text_data=json.dumps({
            'type': 'user_online',
            'username': event['username'],
            'action': event['action']
        }))

    @database_sync_to_async
    def save_message(self, message_content):
        """
        Saves message to database.
        Returns the created Message object.
        """
        room, created = Room.objects.get_or_create(name=self.room_name)
        message = Message.objects.create(
            room=room,
            user=self.user,
            content=message_content
        )
        return message