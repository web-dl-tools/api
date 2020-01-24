"""
Db (abstract) models.
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class IdMixin(models.Model):
    """
    Primary ID mixin.
    """
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """
        Meta properties.
        """
        abstract = True


class CreatedAtMixin(models.Model):
    """
    Created at mixin.
    """
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        """
        Meta properties.
        """
        abstract = True


class ModifiedAtMixin(models.Model):
    """
    Modified at mixin.
    """
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        """
        Meta properties.
        """
        abstract = True
