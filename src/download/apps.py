"""
Download apps.

This file defines the current app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class DownloadAppConfig(AppConfig):
    """
    Download app config.
    """
    name = 'src.download'
    verbose_name = "Download"

    def ready(self):
        from . import signals
