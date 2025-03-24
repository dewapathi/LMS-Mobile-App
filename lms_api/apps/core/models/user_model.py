from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_STUDENT = "student"
    USER_TYPE_TEACHER = "teacher"
    USER_TYPE_ADMIN = "admin"

    USER_TYPE_CHOICES = [
        (USER_TYPE_STUDENT, "student"),
        (USER_TYPE_TEACHER, "teacher"),
        (USER_TYPE_ADMIN, "admin"),
    ]

    id = models.AutoField(auto_created=True, primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_STUDENT)
    is_verified = models.BooleanField(default=False)
    
    # Required by Django for authentication
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tell Django how to login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    bio = models.TextField(blank=True)
    
    class Meta:
        db_table = "profiles"
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"