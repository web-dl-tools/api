"""
Authentication app config.

This file defines the authentication app configuration. For more information see
https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
"""
from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    """
    Authentication app config.
    """

    name = "src.authentication"
    verbose_name = "Authentication"
