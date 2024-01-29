from templated_mail.mail import BaseEmailMessage
from . models import *



def assignment_due_date_email(user, assignment_title, date_given, date_to_be_submitted):
    try:
        message = BaseEmailMessage(
            template_name="api/assignment.html",
            context = {
                "user": user,
                "assignment_title": assignment_title,
                "date_given": date_given,
                "date_to_be_submitted": date_to_be_submitted,
            },
        )
        message.send(["pogooluwa12@gmail.com"])
        print("Sent...")
    except Exception as e:
        return print("Failed", e)
    