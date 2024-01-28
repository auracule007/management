# useractivity/models.py
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20)  # e.g., 'Success' or 'Failed'
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
