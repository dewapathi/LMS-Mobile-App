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


class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log API requests and responses.
    """
    def process_request(self, request):
        try:
            # Decode the request body (if present)
            request_body = request.body.decode("utf-8")
            if 'application/json' in request.META.get('CONTENT_TYPE', ''):
                request_body = json.loads(request_body)
        except Exception as e:
            request_body = f"Could not decode: {e}"

        # Log the request details
        request_logger.info({
            "event": "request",
            "method": request.method,
            "path": request.get_full_path(),
            "headers": {k: v for k, v in request.META.items() if k.startswith('HTTP_') or k.startswith('USER') or k.startswith('LOGNAME') or k.startswith('REMOTE_ADDR') },
            "body": request_body,
        })

    def process_response(self, request, response):
        try:
            # Decode the response content (if applicable)
            response_content = response.content.decode("utf-8")
            if "application/json" in response.get('Content-Type', ''):
                response_content = json.loads(response_content)
        except Exception as e:
            response_content = f"Could not decode: {e}"

        # Log the response details
        response_logger.info({
            "event": "response",
            "status_code": response.status_code,
            "path": request.get_full_path(),
            "headers": {k: v for k, v in request.META.items() if k.startswith('HTTP_') or k.startswith('USER') or k.startswith('LOGNAME') or k.startswith('REMOTE_ADDR') },
            "response": response_content,
        })
        return response