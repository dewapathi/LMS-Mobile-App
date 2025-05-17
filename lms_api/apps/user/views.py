from django.conf import settings
from django.apps import apps

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions

from lms_api.apps.user.serializers import UserSerializer
from lms_api.resources.enum.user_enum import UserRoleEnum


class MeView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class IsAdminRole(permissions.BasePermission):
    """
    Allow only users with role == 'admin'
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRoleEnum.ADMIN.value
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRoleEnum.ADMIN.value


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    queryset = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(is_verified=True)
    http_method_names = ["get", "delete"]
