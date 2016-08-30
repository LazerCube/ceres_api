from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django_extensions.db.fields import AutoSlugField
from core.mixins import UUIDIdMixin

class AccountManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('email'):
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('password'):
            raise ValueError('Users must have a valid password.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(kwargs.get('email', None)),
            username=kwargs.get('username', None),
            first_name=kwargs.get('first_name', ''),
            last_name=kwargs.get('last_name', ''),
        )

        account.set_password(kwargs.get('password'))
        account.save()

        return account

    def create_superuser(self, **kwargs):
        account = self.create_user(**kwargs)

        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser, PermissionsMixin, UUIDIdMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    slug = AutoSlugField(('slug'), populate_from='username')

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
