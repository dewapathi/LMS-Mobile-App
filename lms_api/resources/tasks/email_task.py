from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

__all__ = ("send_email_task",)


@shared_task
def send_email_task(subject, message, recipient_email):
    """
    Celery task to send an email asynchronously.
    This can be used for verification, password reset, notifications, etc.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
