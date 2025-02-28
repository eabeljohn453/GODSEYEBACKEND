from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def __str__(self):
        return f"{self.username} ({self.user_type})"

# Detection Model - Tracks detected threats (Knives, Guns, etc.)
class Detection(models.Model):
    detected_at = models.DateTimeField(auto_now_add=True)
    threat_type = models.CharField(max_length=255)  # e.g., 'Knife', 'Gun'

    def __str__(self):
        return f"{self.threat_type} detected at {self.detected_at}"

# Detection History - Stores general event history (Threats, Landslides, etc.)
class DetectionHistory(models.Model):
    detection_type = models.CharField(max_length=100)  # e.g., 'Threat', 'Landslide'
    detected_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"{self.detection_type} at {self.detected_at}"

# Threat Messages - Alerts generated when a threat is detected
class ThreatMessage(models.Model):
    detection_history = models.ForeignKey(DetectionHistory, on_delete=models.CASCADE, related_name='threat_messages')
    message = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Threat Alert: {self.message} at {self.detected_at}"

# General Message Model (for user notifications)
class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.content[:50]}... at {self.created_at}"  # Shows preview
