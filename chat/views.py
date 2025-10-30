"""
REST API views for chat functionality.
Provides endpoints for message history and room listing.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.responses import success_response, error_response
from .models import Room, Message
from .serializers import MessageSerializer, RoomSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_room_messages(request, room_name):
    """
    Get message history for a specific room.
    Returns last 50 messages ordered by timestamp.
    """
    try:
        room = Room.objects.get(name=room_name)
        messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
        messages = reversed(messages)
        serializer = MessageSerializer(messages, many=True)
        return success_response(
            data=serializer.data,
            message=f"Messages for room {room_name}"
        )
    except Room.DoesNotExist:
        return success_response(
            data=[],
            message=f"Room {room_name} has no messages yet"
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rooms(request):
    """
    List all active chat rooms.
    Returns rooms with message count.
    """
    rooms = Room.objects.filter(is_active=True)
    serializer = RoomSerializer(rooms, many=True)
    return success_response(
        data=serializer.data,
        message="Active chat rooms"
    )