"""
User models.

This file contains an extension on the Django admin user.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.db.models import CreatedAtMixin, ModifiedAtMixin, IdMixin


class User(ModifiedAtMixin, IdMixin, AbstractUser):
    """
    A user entity which extends the Django admin user in order to implement additional custom fields.
    """
    technical = models.BooleanField(_('technical'), default=False)

    class Meta:
        db_table = "user"

    @property
    def full_name(self) -> str:
        """
        :return: a str containing the user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip() if self.first_name else self.username


class Log(CreatedAtMixin, IdMixin):
    """
    A user log entity which logs all API calls.
    """

    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_PUT = "PUT"
    METHOD_PATCH = "PATCH"
    METHOD_DELETE = "DELETE"

    METHODS = (
        (METHOD_GET, METHOD_GET),
        (METHOD_POST, METHOD_POST),
        (METHOD_PUT, METHOD_PUT),
        (METHOD_PATCH, METHOD_PATCH),
        (METHOD_DELETE, METHOD_DELETE),
    )

    user = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.CASCADE
    )
    method = models.CharField(
        _("method"), max_length=15, choices=METHODS
    )
    url = models.TextField(_("url"))
    data = models.JSONField(_("data"), default=dict, null=True)
