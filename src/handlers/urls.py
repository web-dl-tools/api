"""
Handlers urls.

This file contains a url definition for the HandleView() view.
Most other model handling and url config is done through a viewset.
"""
from django.urls import path

from .views import GetHandlerStatusesView

urlpatterns = [
    path("statuses", GetHandlerStatusesView.as_view()),
]
