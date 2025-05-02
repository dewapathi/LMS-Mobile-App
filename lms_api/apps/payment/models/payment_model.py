from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_TYPE_PENDING = "pending"
    STATUS_TYPE_COMPLETED = "completed"
    STATUS_TYPE_FAILED = "failed"

    STATUS_TYPE = [
        (STATUS_TYPE_PENDING, "Pending"),
        (STATUS_TYPE_COMPLETED, "Completed"),
        (STATUS_TYPE_FAILED, "Failed"),
    ]
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_payments",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        settings.COURSE_MODEL, on_delete=models.CASCADE, related_name="course_payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_TYPE, default=STATUS_TYPE_PENDING
    )
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.status}"
