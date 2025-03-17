from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    USER_TYPE_STUDENT = "student"
    USER_TYPE_TEACHER = "teacher"
    USER_TYPE_ADMIN = "admin"

    USER_TYPE_CHOICES = [
        (USER_TYPE_STUDENT, "student"),
        (USER_TYPE_TEACHER, "teacher"),
        (USER_TYPE_ADMIN, "admin"),
    ]

    id = models.AutoField(auto_created=True, primary_key=True)
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
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        """
        Hashes and sets the user's password.
        """
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """
        Checks if the given raw password matches the hashed password.
        """
        return check_password(raw_password, self.password)
