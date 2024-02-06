from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz.models import AssignmentSubmission, Question
from api.models import Enrollment
from .models import PointSystem


@receiver(post_save, sender=AssignmentSubmission)
def award_points_for_assignment_submission(sender, instance, created, **kwargs):
    try:
        if created and instance.is_completed:
            user = instance.user
            points_earned = instance.points
            PointSystem.objects.create(
                user=user, assignment_submission=instance, points_earned=points_earned
            )
    except Exception as e:
        print("Error creating why submitting assignment: ", e)


@receiver(post_save, sender=Enrollment)
def award_badges_for_course_completion(sender, instance, created, **kwargs):
    try:
        if not created and instance.completion_status:
            pass
    except Exception as e:
        print('Error creating BadgeAward instance: ', e)
        
# @receiver(post_save, sender=Question)
# def award_points_for_question(sender, instance, created, **kwargs):
#     if created and instance.is_completed:
#         user = instance.user
#         points_earned = instance.points_awarded
#         PointSystem.objects.create(user=user, question=instance, points_earned=points_earned)
