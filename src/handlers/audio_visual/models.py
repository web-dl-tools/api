"""
Audio visual handler models.
"""
from typing import Type

from django.db import models
from django.utils.translation import gettext_lazy as _

from .handlers import AudioVisualHandler
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler


class AudioVisualRequest(BaseRequest):
    """
    Audio visual handler request model.
    """
    format_selection = models.CharField(_('format selection'), max_length=15)

    class Meta:
        """
        Model metadata.
        """
        db_table = 'audio_visual_request'

    @staticmethod
    def get_handler_object() -> Type[BaseHandler]:
        """
        Get the handler for the request.

        :return: BaseHandler
        """
        return AudioVisualHandler

    def get_name(self) -> str:
        """
        Get the handler verbose/url name.

        :return: str
        """
        return 'audio_visual'
