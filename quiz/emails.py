from django.conf import settings
from templated_mail.mail import BaseEmailMessage
from .models import Assignment,AssignmentSubmission


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

def send_assignment_submissions_email(assignment_id,submission_context):
    try:
        assignment_submissions=AssignmentSubmission.objects.filter(assignment_id=assignment_id).first()
        instructor_email = assignment_submissions.assignment.instructor.user.email
        title = assignment_submissions.assignment.assignment_title
        user = assignment_submissions.user
        date_submitted = assignment_submissions.date_submitted
        message = BaseEmailMessage(
            template_name="quiz/send_assignment_submission_email.html",
            context={
                "email": instructor_email,
                "user":user,
                "title":title,
                "submission_context": submission_context,
                "date_submitted": date_submitted,
            },
        )
        message.send([instructor_email])
        print("Sent")
    except Exception as e:
        print("Failed", e)

def send_assignment_submission_completion_email(is_completed):
    try:
        assignment_submissions=AssignmentSubmission.objects.filter(is_completed=is_completed).first()
        title = assignment_submissions.assignment.assignment_title
        user = assignment_submissions.user
        points = assignment_submissions.points  
        
        date_submitted = assignment_submissions.date_submitted
        message = BaseEmailMessage(
            template_name="quiz/send_assignment_submission_update_email.html",
            context={
                "points": points,
                "user":user,
                "title":title,
                "is_completed": is_completed,
                "date_submitted": date_submitted,
            },
        )
        message.send([user.email])
        print("Sent")
    except Exception as e:
        print("Failed", e)