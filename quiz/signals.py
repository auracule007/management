from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError
from performance.models import UserPerformance
from .models import *


@receiver(post_save, sender=AssignmentSubmission)
def create_award_for_assignment_submission(sender, instance, created, **kwargs):
    if created:
        assignment = instance.assignment
        total_submissions = assignment.assignmentsubmission_set.count()
        completed_submissions = assignment.assignmentsubmission_set.filter(
            is_completed=True
        ).count()
        if total_submissions > 0 and total_submissions == completed_submissions:
            AwardForAssignmentSubmission.objects.create(
                assignment_submission=instance,
                award_name=f"Award for {assignment.assignment_title}",
            )


@receiver(post_save, sender=AssignmentSubmission)
def update_user_performance(sender, instance, created, **kwargs):
    try:
        if created and instance.is_completed:
            user_id = instance.user.id
            user_performance, _ = UserPerformance.objects.get_or_create(user_id=user_id)
            user_performance.calculate_overall_performance_percentage(user_id)
            user_performance.update_performance_percentage(user_id)
            user_performance.save()
    except IntegrityError as e:
        print("Integrity error occurred:", e)
        

@receiver(post_save, sender=QuizSubmission)
def create_award_for_quiz_submission(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        total_submissions = question.quizsubmission_set.count()
        completed_submissions = question.quizsubmission_set.filter(
            is_completed=True
        ).count()
        if total_submissions > 0 and total_submissions == completed_submissions:
            AwardForQuizSubmission.objects.create(
                quiz_submission=instance, award_name=f"Award for {question.title}"
            )
