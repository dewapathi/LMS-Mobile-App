from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from rest_framework import serializers

from lms_api.apps.core.models import User
from lms_api.apps.core.resources.services import get_tokens_for_user

from lms_api.resources.signals import user_create


class CreateAddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=255, required=False)
    zip_code = serializers.CharField(max_length=255, required=False)


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    role = serializers.CharField()

    address = CreateAddressSerializer(write_only=True)

    def validate(self, data):
        """Ensure the email is unique"""

        if User.objects.filter(
            Q(email=data["email"]) | Q(username=data["username"])
        ).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    def create(self, validated_data):
        """Create the user inside a database transaction"""
        with transaction.atomic():
            validated_data["password"] = make_password(validated_data["password"])
            address = validated_data.pop("address")

            user_create.send(
                sender=self.__class__, user=validated_data, address=address
            )

            validated_data["address"] = validated_data

            return validated_data


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
            tokens = get_tokens_for_user(user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password.")

        return tokens
