"""
Download consumers.

This file contains the Channels (websockets) consumers to handle connection event
and data/message events and handling.
"""
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token


class RequestConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        dict_data = json.loads(text_data)
        if dict_data["type"] == "requests.group.join":
            token = Token.objects.get(key=dict_data["content"])
            if token:
                async_to_sync(self.channel_layer.group_add)(
                    f"requests.group.{token.user.id}", self.channel_name
                )
                self.send(
                    text_data=json.dumps(
                        {
                            "type": "requests.group.joined",
                            "content": f"requests.group.{token.user.id}",
                        }
                    )
                )

    def websocket_send(self, event):
        self.send(
            text_data=json.dumps(
                {"type": event["data"]["type"], "content": event["data"]["message"]}
            )
        )
