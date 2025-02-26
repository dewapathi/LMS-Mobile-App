from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    student = models.ForeignKey(
        settings.AUTH_CORE_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        settings.COURSE_MODEL, on_delete=models.CASCADE, related_name="enrollments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "enrollments"
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.email} -> {self.course.title}"
