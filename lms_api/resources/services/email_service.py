from lms_api.resources.tasks.email_task import send_email_task

__all__ = ("send_lms_email",)


def send_lms_email(subject, message, to_email):
    """
    Common email sending function to be used across the app.
    This function is called by Celery tasks.
    """
    send_email_task.delay(subject, message, to_email)
