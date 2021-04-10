"""
Download channels.

This file contain Channels (websockets) socket url definitions
for the Channels consumers.
"""
from django.urls import re_path

from .consumers import RequestConsumer

websocket_urlpatterns = [
    re_path(r"ws/requests", RequestConsumer.as_asgi()),
]
