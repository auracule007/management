from django.db import models

from api.models import User
from quiz.models import AssignmentSubmission, Question, QuizSubmission


class PointSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_earned = models.PositiveIntegerField(default=0)
    assignment_submission = models.ForeignKey(
        AssignmentSubmission, on_delete=models.CASCADE, null=True, blank=True
    )
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Points - {self.points_earned} for {self.user.username}"


class QuizSubmissionPointSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_earned = models.PositiveIntegerField(default=0)
    quiz_submission = models.ForeignKey(
        QuizSubmission, on_delete=models.CASCADE, null=True, blank=True
    )
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QuizPoints - {self.points_earned} for {self.user.username}"


class Badge(models.Model):
    name = models.CharField(max_length=100)    
    def __str__(self):
        return self.name    
    
class BadgeAward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name}::{self.badge.name}'
    