"""
Download admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
from django.contrib import admin
from .models import BaseRequest


@admin.register(BaseRequest)
class BaseRequestAdmin(admin.ModelAdmin):
    """
    BaseRequest admin.
    """
