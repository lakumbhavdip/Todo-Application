
from todo_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def send_email(subject, body, recipient_email):
    message = body
    recipient = recipient_email
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER, 
        [recipient],
        fail_silently=False,
        html_message=body
    )