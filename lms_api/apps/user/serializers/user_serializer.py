from django.conf import settings
from django.apps import apps

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ["id", "username", "email", "first_name", "last_name", "role", "is_verified"]