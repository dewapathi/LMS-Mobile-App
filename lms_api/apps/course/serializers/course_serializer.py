from rest_framework import serializers

from lms_api.apps.course import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = "__all__"