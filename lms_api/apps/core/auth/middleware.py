import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# Get separate loggers for requests and responses
request_logger = logging.getLogger("api.request")
response_logger = logging.getLogger("api.response")


class APIKeyMiddleware:
    """
    Middleware to check for the API key in the request headers for specific paths.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths to exclude from API key validation
        excluded_paths = ["/admin", "/health"]

        # Skip API key validation for excluded paths
        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)

        # Check API key for paths starting with "/api/"
        if request.path.startswith("/api/"):
            api_key = request.headers.get("X-API-KEY")
            if not api_key or api_key != settings.API_KEY:
                return JsonResponse({"error": "Invalid API Key"}, status=403)

        # Continue processing the request
        return self.get_response(request)