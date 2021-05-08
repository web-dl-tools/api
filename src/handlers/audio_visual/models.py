"""
Audio visual handler models.

This file contains the BaseRequest implementation for the audio visual handler.
"""
from typing import Type

from django.db import models
from django.utils.translation import gettext_lazy as _

from .handlers import AudioVisualHandler
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler


class AudioVisualRequest(BaseRequest):
    """
    An audio visual handler request model which implements the BaseRequest object.
    """

    format_selection = models.CharField(_("format selection"), max_length=50)
    output = models.CharField(_("output"), max_length=100)
    audio_format = models.CharField(_("audio format"), max_length=20, null=True)

    class Meta:
        """
        Model metadata.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """

        db_table = "audio_visual_request"

    @staticmethod
    def get_handler_object() -> Type[BaseHandler]:
        """
        Return the type of the associated handler. This method is called when retrieving
        the type of the associated handler object in order to perform a static function call.

        :return: a Type[BaseHandler] of the BaseHandler object.
        """
        return AudioVisualHandler
