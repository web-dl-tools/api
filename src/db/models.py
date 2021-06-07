"""
Db (abstract) models.

This file contains commonly used db model fields in abstract mixin classes.
They can be used to automatically add commonly used fields to models.
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class IdMixin(models.Model):
    """
    A primary ID mixin that adds a unique UUID4 id on object creation.
    """
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True


class CreatedAtMixin(models.Model):
    """
    A created at mixin that adds a created_at datetime field
    with the object creation datetime automatically filled in.
    """
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True


class ModifiedAtMixin(models.Model):
    """
    a Modified at mixin that adds a modified_at datetime field
    which automatically gets updated with the current datetime at each object save.
    """
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        """
        Meta properties.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overwrite .save() to automatically update the modified_at property.
        """
        self.modified_at = timezone.now()
        if update_fields:
            update_fields.append('modified_at')

        super().save(force_insert, force_update, using, update_fields)
