"""
Download apps.
"""
from django.apps import AppConfig


class DownloadAppConfig(AppConfig):
    """
    Download app config.
    """
    name = 'src.download'

    def ready(self):
        from . import signals
