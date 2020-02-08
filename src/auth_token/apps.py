"""
Auth token app config.

This file defines the auth token app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class AuthTokenAppConfig(AppConfig):
    """
    Auth token app config.
    """

    name = "src.auth_token"
    verbose_name = "Auth Token"
