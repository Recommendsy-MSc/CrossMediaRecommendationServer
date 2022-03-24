from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..managers import CustomUserManager

class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "Email Already Exists"
        }
    )

    username = models.CharField(
        max_length=16,
        unique=True,
        error_messages={
            'unique': "Username already taken"
        }
    )

    name = models.CharField(max_length=30)
    birth_year = models.CharField(max_length=4)
    password = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'name',
        'username'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = 'crm_app_usermodel'