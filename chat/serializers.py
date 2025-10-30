"""
Serializers for chat models.
"""

from rest_framework import serializers
from .models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with user details.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'username', 'content', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for Room model with message count.
    """
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'created_at', 'is_active', 'message_count']
        read_only_fields = ['id', 'created_at']

    def get_message_count(self, obj):
        return obj.messages.count()