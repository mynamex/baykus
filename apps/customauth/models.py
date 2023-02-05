from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models

from apps import accounts


class MyUserManager(BaseUserManager):
    def create_user(self, username,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name='Username')
    name = models.CharField(max_length=40, blank=True)

    account = models.ForeignKey('accounts.Account', null=True, related_name="myuser", on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of customer?"
        # Simplest possible answer: All admins are customer
        return self.is_admin


    def get_short_name(self):
        return self.name