from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz.models import AssignmentSubmission

from .handlers import *
from .models import UserPerformance


@receiver(post_save, sender=AssignmentSubmission)
def assignment_completed_handler(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        update_user_performance(user)


@receiver(post_save, sender=Quiz)
def quiz_completed_handler(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        update_user_performance(user)
