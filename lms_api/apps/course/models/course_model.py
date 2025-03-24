from django.db import models
from django.conf import settings

from .course_category import CourseCategory
from lms_api.apps.core.models import User


class Course(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_courses", null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.title
    
class CourseContent(models.Model):
    CONTENT_TYPES = [
        ('VIDEO', 'Video'),
        ('PDF', 'PDF'),
        ('QUIZ', 'Quiz'),
        ('TEXT', 'Text'),
    ]
    id = models.AutoField(auto_created=True, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=200)
    content_type = models.FileField(upload_to="course_contents/", choices=CONTENT_TYPES)
    file = models.URLField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["order"]
        db_table = "course_contents"
    
    def __str__(self):
        return f"{self.course.title} {self.title}"

