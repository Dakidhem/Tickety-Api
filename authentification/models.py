from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('FR_ASSISTANT', 'FR Assistant'),
        ('DZ_ASSISTANT', 'DZ Assistant'),
        ("ADMIN","Administrateur")
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)