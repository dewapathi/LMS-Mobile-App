from django.db import models

import uuid


class User(models.Model):
    USER_TYPE_STUDENT = "student"
    USER_TYPE_TEACHER = "teacher"
    USER_TYPE_ADMIN = "admin"

    USER_TYPE_CHOICES = [
        (USER_TYPE_STUDENT, "student"),
        (USER_TYPE_TEACHER, "teacher"),
        (USER_TYPE_ADMIN, "admin"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, null=False)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_STUDENT
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
