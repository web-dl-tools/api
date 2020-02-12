"""
Download consumers.

This file contains the Channels (websockets) consumers to handle connection event
and data/message events and handling.
"""
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "unique_group_name", self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "unique_group_name", self.channel_name
        )

    def websocket_send(self, event):
        self.send(
            text_data=json.dumps(
                {"type": event["data"]["type"], "content": event["data"]["message"]}
            )
        )
