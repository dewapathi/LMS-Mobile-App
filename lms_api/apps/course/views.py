from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from lms_api.apps.course import serializers, models

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Course.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CourseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = models.CourseCategory.objects.all()
    
    def get_queryset(self):
        return self.queryset