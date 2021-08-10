"""
Application admin.

This file defines the Django admin structure for the package models. For more info see
https://docs.djangoproject.com/en/3.0/ref/django-admin/
"""
from django.contrib import admin

admin.site.site_url = ''  # Removes the 'View Site' link
admin.site.site_header = 'Web DL administration'
