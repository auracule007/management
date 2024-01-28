from .models import UserPerformance
from api.models import User
from quiz.models import Assignment,Question


def calculate_progress_percentage(user):
    total_activities = Assignment.objects.filter(user=user, is_completed=True).count() + \
                       Question.objects.filter(user=user, is_completed=True).count()
    total_possible_activities = Assignment.objects.filter(user=user).count() + \
                                 Question.objects.filter(user=user).count()

    if total_possible_activities == 0:
        return 0  # Avoid division by zero error

    progress_percentage = (total_activities / total_possible_activities) * 100
    return progress_percentage


def calculate_completion_status(user):
    all_assignments_completed = Assignment.objects.filter(user=user, is_completed=True).exists()
    all_questions_completed = Question.objects.filter(user=user, is_completed=True).exists()

    if all_assignments_completed and all_questions_completed:
        return "Completed"
    else:
        return "In Progress"


def update_user_performance(user):
    user_performance, created = UserPerformance.objects.get_or_create(user=user)
    user_performance.progress_percentage = calculate_progress_percentage(user)
    user_performance.completion_status = calculate_completion_status(user)
    user_performance.save()



      