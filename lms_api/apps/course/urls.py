from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CourseViewSet,CourseCategoryViewSet

router = DefaultRouter()
router.register("course", CourseViewSet)
router.register("course-category", CourseCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls))
]
