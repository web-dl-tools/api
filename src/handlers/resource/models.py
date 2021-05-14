"""
Resource handler models.

This file contains the BaseRequest implementation for the resource handler.
"""
from typing import Type

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from .handlers import ResourceHandler
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler


class ResourceRequest(BaseRequest):
    """
    A resource handler request model which implements the BaseRequest object.
    """
    extensions = ArrayField(models.CharField(max_length=20), verbose_name="extensions")
    min_bytes = models.IntegerField(_("min bytes"), default=0)
    delay = models.IntegerField(_("delay"), default=0)

    class Meta:
        """
        Model metadata.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """

        db_table = "resource_request"

    @staticmethod
    def get_handler_object() -> Type[BaseHandler]:
        """
        Return the type of the associated handler. This method is called when retrieving
        the type of the associated handler object in order to perform a static function call.

        :return: a Type[BaseHandler] of the BaseHandler object.
        """
        return ResourceHandler
