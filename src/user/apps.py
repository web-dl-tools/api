"""
User app config.

This file defines the current app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    User app config.
    """

    name = "src.user"
    verbose_name = "User"
