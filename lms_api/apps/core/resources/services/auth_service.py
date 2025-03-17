from django.conf import settings
from django.utils.http import urlsafe_base64_encode, base36_to_int, int_to_base36
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare

from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken

from lms_api.resources.services.email_service import send_lms_email
from lms_api.apps.users.serializers import UserSerializer


class CustomTokenGenerator():
    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value for the token using user-specific data.
        """
        return(
            str(user.pk) + str(timestamp) + str(user.is_verified)
        )
    
    def make_token(self, user):
        """
        Generate a token for the given user.
        """
        timestamp = int(datetime.now().timestamp())
        hash_value = self._make_hash_value(user, timestamp)
        return f"{int_to_base36(timestamp)}-{hash_value}"
    
    def check_token(self, user, token):
        """
        Validate the token for the given user.
        """
        if not (user and token):
            return False
        
        try:
            ts_b36, hash_value = token.split("-")
            timestamp = base36_to_int(ts_b36)
        except (ValueError, AttributeError):
            return False
        
        expected_hash = self._make_hash_value(user, timestamp)
        if not constant_time_compare(hash_value, expected_hash):
            return False
        
        if (datetime.now().timestamp() - timestamp) > settings.PASSWORD_RESET_TIMEOUT:
            return False
        
        return True
        
custom_token_generator = CustomTokenGenerator()

def get_tokens_for_user(user):
    """
    Generate JWT tokens for the user and include additional user data in the payload.
    """
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
        "user": UserSerializer(user).data
    }


def _generate_verification_token(user):
    """
    Generate a JWT token for email verification.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def send_verification_email(user):
    """
    Send an email with a verification link to the user.
    """
    token = _generate_verification_token(user)
    verification_url = f"{settings.BACKEND_URL}api/verify-email/?token={token}"
    subject = "Verify Your Email Address"
    message = (
        f"Click the link below to verify your email address:\n\n{verification_url}"
    )
    send_lms_email(subject, message, user.email)
    

def _generate_password_reset_token(user):
    """
    Generate a password reset token using the custom token generator.
    """
    return custom_token_generator.make_token(user)

def send_password_reset_email(user):
    """
    Send an email with a password reset link to the user.
    """
    token = _generate_password_reset_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.BACKEND_URL}api/reset-password/{uidb64}/{token}/"
    subject = "Reset your password"
    message = f"Click the link below to reset your password:\n\n{reset_link}"
    send_lms_email(subject, message, user.email)
    
