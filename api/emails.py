from django.conf import settings
from management.dev import *
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from . models import *


def update_course_email(category, name, description, requirements1):
    try:
        message = BaseEmailMessage(
            template_name="api/send_email.html",
            context={
                "category": category,
                "description": description,
                "name": name,
                "requirements1": requirements1,
            },
        )
        message.send(['pogooluwa12@gmail.com'])
        print("Sent")
    except Exception as e:
        print("Failed", e)
   
