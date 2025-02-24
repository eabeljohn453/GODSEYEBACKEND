from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  # Extending AbstractUser
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def __str__(self):
        return self.username
