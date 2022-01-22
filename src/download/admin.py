"""
Download admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import BaseRequest


@admin.register(BaseRequest)
class BaseRequestAdmin(admin.ModelAdmin):
    """
    BaseRequest admin.
    """
    list_display = ('id', 'status', 'created_at')
    list_filter = ('user', 'created_at')
    fieldsets = (
        (None, {'fields': ('id', 'user', 'status')}),
        (_('Important dates'), {'fields': ('start_processing_at', 'completed_at', 'start_compressing_at', 'compressed_at')}),
    )
    readonly_fields=('id', 'user', 'status', 'start_processing_at', 'completed_at', 'start_compressing_at', 'compressed_at')
