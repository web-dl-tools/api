"""
Handlers urls.

This file contains a url definition for the HandleView() view.
Most other model handling and url config is done through a viewset.
"""
from django.urls import path

from .views import GetFileView

urlpatterns = [
    path("file/<str:path>", GetFileView.as_view()),
    path("file/<str:path>/<str:slug>", GetFileView.as_view()),
]
