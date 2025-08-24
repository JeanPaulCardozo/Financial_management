from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    """Format create user and super user"""

    def create_user(self, email, password=None, **extra_fields):
        """"Create user"""
        if not email:
            raise ValueError("The email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Model User"""
    id_user = models.AutoField(primary_key=True)
    username = None  # Delete field username
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()
