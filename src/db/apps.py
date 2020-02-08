"""
Db app config.

This file defines the current app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class DbAppConfig(AppConfig):
    """
    Db app config.
    """

    name = "src.db"
    verbose_name = "DB"
