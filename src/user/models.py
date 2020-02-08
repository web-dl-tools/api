"""
User models.

This file contains an extension on the Django admin user.
"""
from django.contrib.auth.models import AbstractUser

from src.db.models import ModifiedAtMixin


class User(ModifiedAtMixin, AbstractUser):
    """
    A user entity which extends the Django admin user in order to implement additional custom fields.
    """

    class Meta:
        db_table = "user"
