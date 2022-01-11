from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, username, name, password, **extra_fields):
        if not email:
            raise ValueError("User must have a Email Address")

        if not username:
            raise ValueError("User must have a username")

        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email),
            username=self.username,
            name=self.name,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, username, name, password, **extra_fields):
        return self._create_user(email, username, name, password, **extra_fields)

    def create_superuser(self, email, username, name, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            name=name,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    mob_no = models.CharField(max_length=12, default='')
    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username
