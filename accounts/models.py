from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('explorer', 'Explorer'),
        ('contributor', 'Contributor'),
        ('curator', 'Curator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='explorer')
    bio = models.TextField(blank=True)
    region = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(default=list, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    xp = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
