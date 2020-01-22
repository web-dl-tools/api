"""
User models.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    User entity.
    """
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        db_table = 'user'
