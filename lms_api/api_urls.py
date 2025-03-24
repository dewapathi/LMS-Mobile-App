from django.urls import path, include

urlpatterns = [
    path("", include("lms_api.apps.core.urls")),
    path("", include("lms_api.apps.course.urls"))
]
