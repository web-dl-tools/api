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

    @property
    def full_name(self) -> str:
        """
        :return: a str containing the user's full name.
        """
        return f"{self.first_name} {self.last_name}"
