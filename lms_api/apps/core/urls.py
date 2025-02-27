from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import sign_up, sign_in

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
