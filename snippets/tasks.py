"""Snippet Celery Task"""

# Base imports
from celery import shared_task

# Django imports
from django.core.mail import send_mail
from django_snippets.settings import EMAIL_HOST_USER as sender


@shared_task
def sendEmail(subject, body, email):
    """
    Send an email to user.

    Parameters:
    subject (str): Email subject
    body (str): Email body
    email (str): Recipient's email.

    """
    if not email:
        return

    send_mail(
        subject=subject,
        message=body,
        from_email=sender,
        recipient_list=[email]
    )
