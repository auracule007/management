from django.conf import settings
from management.dev import *
from templated_mail.mail import BaseEmailMessage


def update_course_email(full_name, email, subject, message):
    try:
        message = BaseEmailMessage(
            template_name="api/send_email.html",
            context={
                "full_name": full_name,
                "email": email,
                "subject": subject,
                "message": message,
            },
        )
        message.send([email, settings.EMAIL_HOST])
        print("Sent")
    except Exception as e:
        print("Failed", e)
    return
