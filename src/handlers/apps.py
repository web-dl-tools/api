"""
Handlers app config.

This file defines the handlers app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class HandlersConfig(AppConfig):
    """
    Handlers app config.
    """

    name = "src.handlers"
    verbose_name = "Handlers"
