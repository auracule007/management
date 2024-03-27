from api.models import *
from quiz.models import AssignmentSubmission, Question, QuizSubmission

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

def calculate_quiz_percentage(user):
    total_activities = (
        QuizSubmission.objects.filter(user=user, is_completed=True).count()
        
    )
    total_possible_activities = (
        QuizSubmission.objects.filter(user=user).count()
        
    )

    if total_possible_activities == 0:
        return 0

    progress_percentage = (total_activities / total_possible_activities) * 100
    return progress_percentage


def calculate_quiz_completion_status(user):
    all_assignmentsubmissions_completed = QuizSubmission.objects.filter(
        user=user, is_completed=True
    ).exists()
    # all_questions_completed = Question.objects.filter(
    #     user=user, is_completed=True
    # ).exists()

    if all_assignmentsubmissions_completed:
        return "Completed"
    else:
        return "Uncompleted"


def update_user_performance(user_id):
    overall_percentage = UserPerformance.calculate_overall_performance_percentage(user_id)
    user_performance, created = UserPerformance.objects.get_or_create(user_id=user_id)
    user_performance.progress_percentage = overall_percentage
    user_performance.save()

    # Award rewards based on progress percentage
    if overall_percentage <= 39:
        ModulesHighFive.objects.create(user=user_performance.user)
    elif 40 <= overall_percentage <= 50:
        PointForEachModule.objects.create(user=user_performance.user)
    elif 51 <= overall_percentage <= 60:
        GemForEachPoint.objects.create(user=user_performance.user)
    elif 70 <= overall_percentage <= 90:
        coin = Coin.objects.create(user=user_performance.user)
        Token.objects.create(user=user_performance.user, coin=coin)
    elif 90 <= overall_percentage <= 100:
        Token.objects.create(user=user_performance.user, coin=None)

# def update_user_performance(user_id):
#     overall_percentage = UserPerformance.calculate_overall_performance_percentage(user_id)
#     user_performance, created = UserPerformance.objects.get_or_create(user_id=user_id)
#     user_performance.progress_percentage = overall_percentage
#     user_performance.save()

#     # Award rewards based on progress percentage
#     if overall_percentage <= 39:
#         ModulesHighFive.objects.create(user=user_id)
#     elif 40 <= overall_percentage <= 50:
#         PointForEachModule.objects.create(user=user_id)
#     elif 51 <= overall_percentage <= 60:
#         GemForEachPoint.objects.create(user=user_id)
#     elif 70 <= overall_percentage <= 90:
#         Coin.objects.create(user=user_id)
#     elif 90 <= overall_percentage <= 100:
#         Token.objects.create(user=user_id)


# def update_user_performance(user):
#     user_performance, created = UserPerformance.objects.get_or_create(user=user)
#     user_performance.progress_percentage = calculate_progress_percentage(user)
#     user_performance.completion_status = calculate_completion_status(user)
#     user_performance.save()
        

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

# def update_user_performance(user_id):
#     user_performance, created = UserPerformance.objects.get_or_create(user_id=user_id)
#     # Calculate the number of each reward type
#     highfives = ModulesHighFive.objects.filter(user=user_performance.user).count()
#     points = PointForEachModule.objects.filter(user=user_performance.user).count()
#     gems = GemForEachPoint.objects.filter(user=user_performance.user).count()
#     coins = Coin.objects.filter(user=user_performance.user).count()
#     tokens = Token.objects.filter(user=user_performance.user).count()

#     # Award rewards based on the current count
#     while highfives >= 5:
#         user_performance.points += 1
#         highfives -= 5

#     while points >= 20:
#         user_performance.gems += 1
#         points -= 20

#     while gems >= 10:
#         user_performance.coins += 1
#         gems -= 10

#     while coins >= 10:
#         user_performance.tokens += 1
#         coins -= 10

#     while tokens >= 10:
#         user_performance.tokens -= 10
#         user_performance.badges += 1

#     user_performance.save()

# def update_user_performance(user_id):
#     overall_percentage = UserPerformance.calculate_overall_performance_percentage(user_id)
#     user_performance, created = UserPerformance.objects.get_or_create(user_id=user_id)
#     user_performance.progress_percentage = overall_percentage
#     user_performance.save()

#     highfives = ModulesHighFive.objects.filter(user=user_performance.user).count()
#     points = PointForEachModule.objects.filter(user=user_performance.user).count()
#     gems = GemForEachPoint.objects.filter(user=user_performance.user).count()
#     coins = Coin.objects.filter(user=user_performance.user).count()
#     tokens = Token.objects.filter(user=user_performance.user).count()

#     # Award rewards based on progress percentage
#     if highfives >= 5:
#         user_performance.points += 1
#         ModulesHighFive.objects.filter(user=user_performance.user).delete()
#     if user_performance.points >= 20:
#         user_performance.gems += 1
#         user_performance.points -= 20
#     if user_performance.gems >= 10:
#         user_performance.coins += 1
#         user_performance.gems -= 10
#     if user_performance.coins >= 10:
#         user_performance.tokens += 1
#         user_performance.coins -= 10
#     if user_performance.tokens >= 10:
#         user_performance.tokens -= 10
#         user_performance.badges += 1

#     user_performance.save()

def update_user_performance_for_modules(user):
    user_performance, created = UserPerformanceForModuleCompletion.objects.get_or_create(user=user)
    user_performance.progress_percentage = calculate_progress_percentage_for_module(user)
    user_performance.completion_status = calculate_completion_status_for_modules(user)
    user_performance.save()

def calculate_score_percentage(user, quiz):
    total_questions = quiz.question.count()
    total_correct = QuizSubmission.objects.filter(
        user=user, question__in=quiz.question.all(), is_completed=True
    ).count()

    if total_questions == 0:
        return 0

    score_percentage = (total_correct / total_questions) * 100
    return score_percentage

