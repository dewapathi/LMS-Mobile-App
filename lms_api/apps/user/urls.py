from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MeView, AdminUserViewSet

router = DefaultRouter()
router.register(r"users", AdminUserViewSet, basename="user")

urlpatterns = [
    path("user/me/", MeView.as_view(), name="user-me"),
    path("", include(router.urls)),
]
