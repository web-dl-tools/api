"""
Authentication admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(TokenProxy)
