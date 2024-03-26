from api.models import Modules, User
from quiz.models import AssignmentSubmission, Question

from .models import UserPerformance, UserPerformanceForModuleCompletion


def calculate_progress_percentage(user):
    total_activities = (
        AssignmentSubmission.objects.filter(user=user, is_completed=True).count()
        
    )
    total_possible_activities = (
        AssignmentSubmission.objects.filter(user=user).count()
        
    )

    if total_possible_activities == 0:
        return 0

    progress_percentage = (total_activities / total_possible_activities) * 100
    return progress_percentage


def calculate_completion_status(user):
    all_assignmentsubmissions_completed = AssignmentSubmission.objects.filter(
        user=user, is_completed=True
    ).exists()
    # all_questions_completed = Question.objects.filter(
    #     user=user, is_completed=True
    # ).exists()

    if all_assignmentsubmissions_completed:
        return "Completed"
    else:
        return "Uncompleted"


def update_user_performance(user):
    user_performance, created = UserPerformance.objects.get_or_create(user=user)
    user_performance.progress_percentage = calculate_progress_percentage(user)
    user_performance.completion_status = calculate_completion_status(user)
    user_performance.save()


def calculate_progress_percentage_for_module(user):
    total_activities = Modules.objects.filter(courses__enrollment__student__user=user,is_completed=True).count()               
    total_possible_activities = Modules.objects.count()
    if total_possible_activities == 0:
        return 0
    progress_percentage = (total_activities / total_possible_activities) * 100
    print(progress_percentage)
    return progress_percentage

def calculate_completion_status_for_modules(user):
    all_module_completed = Modules.objects.filter(
        courses__enrollment__student__user=user, is_completed=True
    ).exists()

    if all_module_completed:
        return True
    else:
        return False

def update_user_performance_for_modules(user):
    user_performance, created = UserPerformanceForModuleCompletion.objects.get_or_create(user=user)
    user_performance.progress_percentage = calculate_progress_percentage_for_module(user)
    user_performance.completion_status = calculate_completion_status_for_modules(user)
    user_performance.save()
