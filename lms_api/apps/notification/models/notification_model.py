from django.conf import settings
from django.db import models


class Notification(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_CORE_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"Notification for {self.user.email}"
