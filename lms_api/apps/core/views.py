from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from sentry_sdk import capture_exception

from lms_api.apps.core import serializers, models
from lms_api.apps.core.docs.swagger_doc import (
    sign_up_schema,
    sign_in_schema,
    verify_email_schema, forgot_password_schema, reset_password_schema
)
from lms_api.apps.core.resources.services import send_password_reset_email,auth_service


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
        capture_exception(e)
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
        capture_exception(e)
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
    

@forgot_password_schema
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = serializers.ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        
        try:
            user = models.User.objects.get(email=email)
            send_password_reset_email(user)
            
            return Response({"message": "Password reset link has been sent."}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@reset_password_schema
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, token):
    serializer = serializers.ResetPasswordSerializer(data=request.data)
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = models.User.objects.get(pk=user_id)
        
        if auth_service.jwt_token_generator.check_token(user, token):
            if serializer.is_valid():
                new_password = serializer.validated_data["new_password"]
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
        

        
        
        
        
        
        
        