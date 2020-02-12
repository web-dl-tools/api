"""
Channels routing.

this file contains routing declaration for Channels (websockets).
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from src.download.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))}
)
