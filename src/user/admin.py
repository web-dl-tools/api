"""
User admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
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
