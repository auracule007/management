from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz.models import AssignmentSubmission, QuizSubmission

from .handlers import *

@receiver(post_save, sender=AssignmentSubmission)
def assignment_completed_handler(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        update_user_performance(user)


@receiver(post_save, sender=QuizSubmission)
def quiz_completed_handler(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        update_user_performance(user)
