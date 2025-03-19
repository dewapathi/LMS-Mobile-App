from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from celery import shared_task

__all__ = ("send_email_task",)


@shared_task(blind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 5})
def send_email_task(subject, message, recipient_email, html_message=None):
    """
    Celery task to send an email asynchronously.
    This can be used for verification, password reset, notifications, etc.
    """
    email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    
    if html_message:
        email.attach_alternative(html_message, "text/html")
        
    email.send()
