"""
Db (abstract) models.

This file contains commonly used db model fields in abstract mixin classes.
They can be used to automatically add commonly used fields to models.
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class IdMixin(models.Model):
    """
    a Primary ID mixin that adds a unique UUID4 id on object creation.
    """
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True


class CreatedAtMixin(models.Model):
    """
    a Created at mixin that adds a created_at datetime field
    with the object creation datetime automatically filled in.
    """
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True


class ModifiedAtMixin(models.Model):
    """
    a Modified at mixin that adds a modified_at datetime field
    which automatically get's updated with the current datetime at each object save.
    """
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True
