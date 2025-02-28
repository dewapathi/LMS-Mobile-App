from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import sign_up, sign_in, verify_email

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("verify-email/", verify_email, name="verify-email"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
