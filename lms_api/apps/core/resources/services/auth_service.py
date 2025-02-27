from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["username"] = user.username
    refresh["email"] = user.email
    refresh["first_name"] = user.first_name
    refresh["last_name"] = user.last_name
    refresh["role"] = user.role
    refresh["is_verified"] = user.is_verified

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }
