"""
Chat models: Room and Message.
Room represents a chat room, Message stores chat history.
"""

from django.db import models
from django.conf import settings


class Room(models.Model):
    """
    Chat room model.
    Each room has a unique name and can be public or private.
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Message model for chat history.
    Links to Room and User, stores message content and timestamp.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username} in {self.room.name}: {self.content[:50]}"