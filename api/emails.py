# from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from . models import *

from management.dev import *


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
        message.send(["f.owolabi81@gmail.com"])
        print("Sent")
    except Exception as e:
        print("Failed", e)

def send_content_upload_mail(content, content_title, content_description, user):
    try:
        message = BaseEmailMessage(
            template_name="api/send_email.html",
            context={
                "content": content,
                "content_title": content_title,
                "content_description": content_description,
                "user": user,
            },
        )
        message.send(["pogooluwa12@gmail.com"])
        print("Sent")
    except Exception as e:
        print("Failed", e)

