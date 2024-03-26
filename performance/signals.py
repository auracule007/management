from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from api.models import Modules
from quiz.models import AssignmentSubmission, QuizSubmission

from .handlers import *

# @receiver(post_save, sender=AssignmentSubmission)
# def assignment_completed_handler(sender, instance, created, **kwargs):
#     if created:
#         user = instance.user
#         update_user_performance(user)


@receiver(post_save, sender=QuizSubmission)
def quiz_completed_handler(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        update_user_performance(user)


@receiver(pre_save, sender=Modules)
def pre_module_save_handler(sender, instance, **kwargs):
    print('into the pre_Save')
    if instance.pk:  
        old_instance = Modules.objects.get(pk=instance.pk)
        if old_instance.is_completed != instance.is_completed:
            if not instance.is_completed:
                try:
                    user_performance = UserPerformanceForModuleCompletion.objects.get(user=instance.course.enrollment_set.student.user)
                    user_performance.delete()
                except UserPerformanceForModuleCompletion.DoesNotExist:
                    pass

@receiver(post_save, sender=Modules)
def module_post_save_handler(sender, instance, created, **kwargs):
    print('into the post save')
    if created and instance.is_completed:
        update_user_performance_for_modules(instance.user)
