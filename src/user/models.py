"""
User models.
"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User entity.
    """

    class Meta:
        db_table = 'user'
