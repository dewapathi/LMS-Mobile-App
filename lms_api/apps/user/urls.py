from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import MeView

router = DefaultRouter()

urlpatterns = [path("user/me/", MeView.as_view(), name="user-me")]
