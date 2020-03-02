"""
Torrent handler models.

This file contains the BaseRequest implementation for the torrent handler.
"""
from typing import Type

from .handlers import TorrentHandler
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler


class TorrentRequest(BaseRequest):
    """
    A torrent handler request model which implements the BaseRequest object.
    """

    class Meta:
        """
        Model metadata.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """

        db_table = "torrent_request"

    @staticmethod
    def get_handler_object() -> Type[BaseHandler]:
        """
        Return the type of the associated handler. This method is called when retrieving
        the type of the associated handler object in order to perform a static function call.

        :return: a Type[BaseHandler] of the BaseHandler object.
        """
        return TorrentHandler
