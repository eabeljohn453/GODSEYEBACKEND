from .models import Message, DetectionHistory, ThreatMessage, CustomUser
from django.contrib import admin
admin.site.register(Message)
admin.site.register(DetectionHistory)
admin.site.register(ThreatMessage)
admin.site.register(CustomUser)