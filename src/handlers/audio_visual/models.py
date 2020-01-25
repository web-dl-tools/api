"""
Audio visual handler models.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from .handlers import AudioVisualHandler
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler


class AudioVisualRequest(BaseRequest):
    """
    Audio visual handler request model.
    """
    FORMAT_BEST_VIDEO = 'bestvideo'
    FORMAT_BEST_AUDIO = 'bestaudio'

    FORMATS = (
        (FORMAT_BEST_VIDEO, 'Best quality video-only format'),
        (FORMAT_BEST_VIDEO, 'Best quality audio-only format'),
    )

    format = models.CharField(_('format'), max_length=15, choices=FORMATS, default=FORMAT_BEST_VIDEO)
    randd = models.CharField(_('randdd'), max_length=200)

    class Meta:
        """
        Model metadata.
        """
        db_table = 'audio_visual_request'

    def get_handler(self) -> BaseHandler:
        """
        Get the handler for the request.

        :return: BaseHandler
        """
        return AudioVisualHandler(self)

    def get_name(self) -> str:
        """
        Get the handler verbose/url name.

        :return: str
        """
        return 'audio_visual'
