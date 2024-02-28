from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=User)
def create_user_choice(sender, created, instance, *args, **kwargs):
    if created:
        first_name = instance.first_name
        last_name = instance.last_name
        Profile.objects.create(user=instance, full_name=f"{first_name} {last_name}")
        if instance.user_type == "Student":
            Student.objects.create(
                user=instance, first_name=first_name, last_name=last_name
            )
            instance.save()

        elif instance.user_type == "Instructor":
            Instructor.objects.create(
                user=instance, first_name=first_name, last_name=last_name
            )
            instance.is_staff = True
            instance.save()


# @receiver(post_save, sender=Enrollment)
# def create_user_choice(sender, created, instance, *args, **kwargs):
#     pass