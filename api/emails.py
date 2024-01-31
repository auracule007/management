from django.conf import settings
from templated_mail.mail import BaseEmailMessage

from management.dev import *


def update_course_email(category, name, description, requirements1):
    try:
        message = BaseEmailMessage(
            template_name="api/send_email.html",
            context={
                "category": category,
                "description": description,
                "name": name,
            },
        )
        message.send(["f.owolabi81@gmail.com"])
        print("Sent")
    except Exception as e:
        print("Failed", e)
