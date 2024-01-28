# useractivity/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.signals import user_logged_in
from rest_framework.authtoken.models import Token
from djoser import signals as djoser_signals
from .models import UserActivity

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        ip_address=request.META.get('REMOTE_ADDR'),
        device=request.META.get('HTTP_USER_AGENT'),
        location='TODO: Implement location retrieval',
        status='Logout'
    )

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        ip_address=request.META.get('REMOTE_ADDR'),
        device=request.META.get('HTTP_USER_AGENT'),
        location='TODO: Implement location retrieval',
        status='Success'
    )

@receiver(post_save, sender=Token)
def token_created_callback(sender, instance, created, **kwargs):
    if created:
        user_activity = UserActivity.objects.create(
            user=instance.user,
            ip_address='TODO: Implement IP retrieval',
            device='TODO: Implement device retrieval',
            location='TODO: Implement location retrieval',
            status='Token Generated',
            token=instance
        )
