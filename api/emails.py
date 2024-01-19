from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

# def password_reset_mail(request):
#     subject= "This is a password reset"
#     html_message= render_to_string("api/send_email.html", {""} )

# uid, token


def password_reset_mail(request, user):
    subject = "Password Reset"
    html_message = render_to_string(
        "api/send_email.html",
        {
            "frontend_reset_url": f"https://127.0.0.1:8000/reset-password?uid={user.id}&token={user.auth_token}"
        },
    )
    plain_message = strip_tags(html_message)
    from_email = "daabzpinky@gmail.com"  # Change this to your desired email
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
