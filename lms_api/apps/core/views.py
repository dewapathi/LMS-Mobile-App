from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    print(f"0000000000000000")
    