"""
Resource apps.

This file defines the resource handler app configuration. For more see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class ResourceHandlerAppConfig(AppConfig):
    """
    Resource handler app config.
    """

    name = "src.handlers.resource"
    verbose_name = "Resource"
