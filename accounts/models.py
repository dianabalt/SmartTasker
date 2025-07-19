from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UserCredentials(models.Model):
    USER_TYPES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    class Meta:
        verbose_name_plural = "User Credentials"
