"""
Torrent apps.

This file defines the torrent handler app configuration. For more see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class TorrentHandlerAppConfig(AppConfig):
    """
    Torrent handler app config.
    """

    name = "src.handlers.torrent"
    verbose_name = "Torrent"
