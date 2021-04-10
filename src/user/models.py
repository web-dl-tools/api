"""
User models.

This file contains an extension on the Django admin user.
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from src.db.models import ModifiedAtMixin


class User(ModifiedAtMixin, AbstractUser):
    """
    A user entity which extends the Django admin user in order to implement additional custom fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "user"

    @property
    def full_name(self) -> str:
        """
        :return: a str containing the user's full name.
        """
        return f"{self.first_name} {self.last_name}"
