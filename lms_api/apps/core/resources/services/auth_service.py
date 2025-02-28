from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["username"] = user.username
    refresh["email"] = user.email
    refresh["first_name"] = user.first_name
    refresh["last_name"] = user.last_name
    refresh["role"] = user.role
    refresh["is_verified"] = user.is_verified

    return {
        "message": "Login successful.",
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }


def _generate_verification_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def send_verification_email(user):
    token = _generate_verification_token(user)
    verification_url = f"{settings.BACKEND_URL}/api/verify-email/?token={token}"
    subject = "Verify Your Email Address"
    message = (
        f"Click the link below to verify your email address:\n\n{verification_url}"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
