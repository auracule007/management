from django.db import models
from utils.choices import *




class UserPerformance(models.Model):
    from api.models import User
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    completion_status = models.CharField(
        max_length=50, default="Uncomplete", choices=COMPLETION_STATUS
    )

    def __str__(self):
        return f"{self.user.username} -{self.progress_percentage}"

    @staticmethod
    def calculate_overall_performance_percentage(user_id):
        from quiz.models import AssignmentSubmission
        total_submissions = AssignmentSubmission.objects.filter(user_id=user_id).count()
        total_completed = AssignmentSubmission.objects.filter(user_id=user_id, is_completed=True).count()

        if total_submissions == 0:
            return 0
        
        calculations = (total_completed / total_submissions) * 100
        print('calculations: ', calculations)
        return calculations

    @staticmethod
    def update_performance_percentage(user_id):
        overall_percentage = UserPerformance.calculate_overall_performance_percentage(user_id)
        user_performance, created = UserPerformance.objects.get_or_create(user_id=user_id)
        user_performance.progress_percentage = overall_percentage
        user_performance.save()
        print('user_performance.progress_percentage :', user_performance.progress_percentage )
        # Update completion status if needed
        if user_performance.progress_percentage == 100:
            user_performance.completion_status = "Complete"
        else:
            user_performance.completion_status = "Incomplete"
        user_performance.save()

class UserQuizPerformance(models.Model):
    from api.models import User
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    completion_status = models.CharField(
        max_length=50, default="Uncomplete", choices=COMPLETION_STATUS
    )

    def __str__(self):
        return f"{self.user.username} -{self.progress_percentage}"

    @staticmethod
    def calculate_overall_quiz_performance_percentage(user_id):
        from quiz.models import QuizSubmission
        total_submissions = QuizSubmission.objects.filter(user_id=user_id).count()
        total_completed = QuizSubmission.objects.filter(user_id=user_id, is_completed=True).count()

        if total_submissions == 0:
            return 0
        
        calculations = (total_completed / total_submissions) * 100
        print('calculations: ', calculations)
        return calculations

    @staticmethod
    def update_performance_percentage(user_id):
        overall_percentage = UserQuizPerformance.calculate_overall_quiz_performance_percentage(user_id)
        user_performance, created = UserQuizPerformance.objects.get_or_create(user_id=user_id)
        user_performance.progress_percentage = overall_percentage
        user_performance.save()
        print('user_performance.progress_percentage :', user_performance.progress_percentage )
        # Update completion status if needed
        if user_performance.progress_percentage == 100:
            user_performance.completion_status = "Complete"
        else:
            user_performance.completion_status = "Incomplete"
        user_performance.save()


class UserPerformanceForModuleCompletion(models.Model):
    try:
        from api.models import User
    except Exception as e:
        print(e)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    completion_status = models.CharField(
        max_length=50, default="Uncomplete", choices=COMPLETION_STATUS
    )

    def __str__(self):
        return f"{self.user.username} -{self.progress_percentage}"



    