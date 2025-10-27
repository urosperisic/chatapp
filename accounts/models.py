from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Adds role field for user type distinction
    """
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        help_text='User role in the system'
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin_user(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """Check if token is still valid (1 hour expiry)"""
        if self.is_used:
            return False
        expiry_time = self.created_at + timedelta(hours=1)
        return timezone.now() < expiry_time
    
    def __str__(self):
        return f"Reset token for {self.user.username}"