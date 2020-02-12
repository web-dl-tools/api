"""
Download channels.

This file contain Channels (websockets) socket url definitions
for the Channels consumers.
"""
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/requests/", consumers.ChatConsumer),
]
