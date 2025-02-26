from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from lms_api.apps.core import serializers


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    try:
        serializer = serializers.UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response("User created successfully.", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
