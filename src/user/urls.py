"""
User urls.

This file contains a url definition for the ObtainAuthToken view.
Most other model handling and url config is done through a viewset.
"""
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("authenticate", ObtainAuthToken.as_view()),
]
