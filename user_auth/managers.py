import logging

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Creates, saves a user with passed username and password.
        """
        if not username:
            raise ValueError(_('Username is required and must be set.'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(username, password, **extra_fields)