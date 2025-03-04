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
