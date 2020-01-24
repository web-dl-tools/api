"""
User models.
"""
from django.contrib.auth.models import AbstractUser

from src.db.models import ModifiedAtMixin


class User(ModifiedAtMixin, AbstractUser):
    """
    User entity.
    """
    class Meta:
        db_table = 'user'
