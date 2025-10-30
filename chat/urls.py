"""
URL routing for chat REST API endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.list_rooms, name='list_rooms'),
    path('rooms/<str:room_name>/messages/', views.get_room_messages, name='room_messages'),
]