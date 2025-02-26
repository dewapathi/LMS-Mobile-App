from django.db import models
from django.conf import settings


class Course(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    teacher = models.ForeignKey(
        settings.AUTH_CORE_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.title
