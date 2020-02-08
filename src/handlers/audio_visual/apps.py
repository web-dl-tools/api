"""
Audio visual apps.

This file defines the current app configuration. For more see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class AudioVisualHandlerAppConfig(AppConfig):
    """
    Audio visual handler app config.
    """

    name = "src.handlers.audio_visual"
    verbose_name = "Audio & Visual"
