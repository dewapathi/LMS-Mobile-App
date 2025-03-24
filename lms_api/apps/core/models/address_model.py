from django.db import models
from django.conf import settings


class Address(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="related_address",
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
