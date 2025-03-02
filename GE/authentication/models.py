
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

class Detection(models.Model):
    detected_at = models.DateTimeField(auto_now_add=True)
    threat_type = models.CharField(max_length=255)  # Adjust field as needed

    def __str__(self):
        return f"{self.threat_type} detected at {self.detected_at}"

class ThreatMessage(models.Model):
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
    threat_detected = models.BooleanField(default=False)
    message = models.TextField()

    def __str__(self):
        return self.message

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def __str__(self):
        return self.username

# Message Model
class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# Detection History Model
class DetectionHistory(models.Model):
    detection_type = models.CharField(max_length=100)  # e.g., 'Threat', 'Landslide'
    detected_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"{self.detection_type} at {self.detected_at}"

# ThreatMessage Model
class ThreatMessage(models.Model):
    message = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message 
