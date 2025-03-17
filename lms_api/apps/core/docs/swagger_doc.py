from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from lms_api.apps.core import serializers


# Common Responses
BAD_REQUEST_RESPONSE = openapi.Response(description="Validation error")

# User create
sign_up_schema = swagger_auto_schema(
    method="post",
    request_body=serializers.UserSignUpSerializer,
    responses={
        201: openapi.Response(
            "User succesfully registered", serializers.UserSignUpSerializer
        ),
        400: BAD_REQUEST_RESPONSE,
    },
    operation_summary="Register a new user",
    operation_description="Creates a new user and return that user",
)

# User login
sign_in_schema = swagger_auto_schema(
    method="post",
    request_body=serializers.UserSignInSerializer,
    responses={
        200: openapi.Response(
            "User login successful.", serializers.UserSignInSerializer
        ),
        400: BAD_REQUEST_RESPONSE,
    },
    operation_summary="User Login",
    operation_description="Authenticates a user and returns JWT access & refresh tokens.",
)

# Verify email
verify_email_schema = swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "token",
            openapi.IN_QUERY,
            description="Token for verifying email",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    responses={
        200: openapi.Response("Email verified successfully."),
        400: BAD_REQUEST_RESPONSE,
    },
    operation_summary="Verify Email",
    operation_description="Verifies a user's email using a token.",
)

#Forgot password
forgot_password_schema = swagger_auto_schema(
    method="post",
    request_body=serializers.ResetPasswordSerializer,
    responses={
        200: openapi.Response(
            description="Password reset link sent successfully.",
            examples={
                "application/json": {"message": "Password reset link sent."}
            },
        ),
        404: openapi.Response(
            description="User not found.",
            examples={
                "application/json": {"error": "User not found."}
            },
        ),
        400: openapi.Response(
            description="Bad request."
        ),
    },
    operation_summary="Forgot Password",
    operation_description="Sends a password reset link to the user's registered email address.",
)

#Reset password
reset_password_schema = swagger_auto_schema(
    method="post",
    request_body=serializers.ResetPasswordSerializer,  # Accepts new_password
    responses={
        200: openapi.Response(
            description="Password reset successful.",
            examples={
                "application/json": {"message": "Password reset successful."}
            },
        ),
        400: openapi.Response(
            description="Invalid token or user.",
            examples={
                "application/json": {"error": "Invalid or expired token."}
            },
        ),
    },
    operation_summary="Reset Password",
    operation_description="Resets the password for the user using the provided token and UID.",
)
