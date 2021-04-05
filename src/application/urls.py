"""
Application urls.

This file contains url definitions for application endpoints.
"""
from django.urls import path
from .views import build_info

urlpatterns = [
    path("build", build_info),
]
