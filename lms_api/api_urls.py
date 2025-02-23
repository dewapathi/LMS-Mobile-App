from django.urls import path, include

urlpatterns = [
    path("", include("lms_api.apps.core.urls")),
    # path("course/", include("apps.course.urls"))
]
