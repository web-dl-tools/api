"""
User admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    User admin.
    """
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_staff')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields=('last_login', 'date_joined')
