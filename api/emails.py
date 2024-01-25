from django.conf import settings
from management.dev import *
from templated_mail.mail import BaseEmailMessage
from . models import *



def sendin_course_update(name, instructor_email):
    try:
        instructor = Instructor.objects.get(email=instructor_email)
        student_email = Student.objects.get(user__email=instructor_email).email
        msg = BaseEmailMessage(template_name='templates/send_email.html',
                               context={
                                   'instructor_email': instructor.email,
                                   'name': name,
                                   'email': student_email,
                               })
        msg.send([instructor_email, student_email])
        print(f'Instructor: {instructor.email}')
        print('Received')
        print(f'Student Email: {student_email}')
        print(f'Course: {name}')
        print('Sent')
    except Instructor.DoesNotExist:
        print(f'Instructor not found for email: {instructor_email}')
    except Student.DoesNotExist:
        print(f'Student not found for email: {instructor_email}')
    except Exception as e:
        print('Failed', e)

































































































































# def update_course_email(full_name, email, subject, message):
#     try:
#         message = BaseEmailMessage(template_name='api/send_email.html',
#         context = {
#             'full_name': full_name,
#             'email': email,
#             'subject':subject,
#             'message':message,
#         })
#         message.send([email, settings.EMAIL_HOST])
#         print('Sent')
#     except Exception as e:
        # print('Failed' , e)
    
# def sendin_course_update(name, instructor):
#     try:
#         instructor_email = Student.objects.get(user__email=instructor)
#         msg = BaseEmailMessage(template_name='api/employee_email.html',
#         context = {
#             'employer_email': instructor_email.courses_set.values('courses__instructor__user__email'),
#             'name': name,
#             'email': instructor,
#         })
#         msg.send([instructor, instructor_email])
#         # print(f'Employer: {employer__email.email}')
#         # print('Received')
#         # print(f'Employee: {email}')
#         # print('Sent')
#     except Exception as e:
#         print('Failed' , e)


    # def send_email_student(full_name, email, course_name):
    #     try:
    #         student = Student.objects.get(email=email)  
    #         subject = 'Course Update Notification'
            
    #         message = render_to_string('templates/send_email.html', {
    #             'full_name': full_name,
    #             'course_name': course_name,
    #         })
    #         send_mail(subject, message, 'from_email', [email])
    #         print(f'Student: {email}')
    #         print('Email Sent')
    #     except Exception as e:
    #         print('Failed:', e)

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