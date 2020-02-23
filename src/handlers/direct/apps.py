"""
Direct apps.

This file defines the direct handler app configuration. For more see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class DirectHandlerAppConfig(AppConfig):
    """
    Direct handler app config.
    """

    name = "src.handlers.direct"
    verbose_name = "Direct"
