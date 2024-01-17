from . models import Student,Instructor, User
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_user_choice(sender, created, instance, *args, **kwargs):
    if created:
        if instance.user_type == 'Student':
            Student.objects.create(user=instance)
            instance.save()

        elif instance.user_type == 'Instructor':
            Instructor.objects.create(user=instance)
            instance.is_staff = True
            instance.save()

