from django.conf import settings
from management.dev import *
from templated_mail.mail import BaseEmailMessage


def update_course_email(full_name, email, subject, message):
    try:
        message = BaseEmailMessage(template_name='api/send_email.html',
        context = {
            'full_name': full_name,
            'email': email,
            'subject':subject,
            'message':message,
        })
        message.send([email, settings.EMAIL_HOST])
        print('Sent')
    except Exception as e:
        print('Failed' , e)
    return 

# def send_email_applicant(full_name, email):
#     try:
#         employer_email = Employee.objects.get(user__email=email)
#         msg = BaseEmailMessage(template_name='api/employee_email.html',
#         context = {
#             'employer_email': employer_email.application_set.values('jobs__employer__user__email'),
#             'full_name': full_name,
#             'email': email,
#         })
#         msg.send([email, employer_email])
#         print(f'Employer: {employer__email.email}')
#         print('Received')
#         print(f'Employee: {email}')
#         print('Sent')
#     except Exception as e:
#         print('Failed' , e)