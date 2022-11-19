"""
Authentication urls.

This file contains url definitions for authentication endpoints.
"""
from django.urls import path
from .views import VerifyFileAccessView

urlpatterns = [
    path("verify/file", VerifyFileAccessView.as_view()),
]
