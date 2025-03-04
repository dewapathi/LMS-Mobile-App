from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from lms_api.apps.core import serializers, models
from lms_api.apps.core.docs.swagger_doc import (
    sign_up_schema,
    sign_in_schema,
    verify_email_schema,
)


@sign_up_schema
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    try:
        serializer = serializers.UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@sign_in_schema
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    try:
        serializer = serializers.UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@verify_email_schema
@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get("token")

    if not token:
        return Response(
            {"Error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]

        user = models.User.objects.get(id=user_id)

        user.is_verified = True
        user.save()

        return Response(
            {"message": "Email verified successfully."}, status=status.HTTP_200_OK
        )

    except TokenError:
        return Response(
            {"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
        )
    except models.User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
