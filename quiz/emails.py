from django.conf import settings
from templated_mail.mail import BaseEmailMessage
from .models import Assignment


def send_course_assignment_email(course_id,assignment_title, date_given,date_to_be_submitted):
    try:
        assignment = Assignment.objects.filter(course_id=course_id).first()
        if assignment:
            enrolled_students_emails = assignment.course.enrollment_set.values_list('student__user__email', flat=True)
            email_list = list(enrolled_students_emails)
            email_string = ', '.join(email_list)
            print(email_string)            
        message = BaseEmailMessage(
            template_name="quiz/send_assignment_email.html",
            context={
                "email": enrolled_students_emails,
                "assignment_title": assignment_title,
                "date_given": date_given,
                "date_to_be_submitted":date_to_be_submitted
            },
        )
        message.send([email_string])
        print("Sent")
    except Exception as e:
        print("Failed", e)
