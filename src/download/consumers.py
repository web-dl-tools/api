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
    """
    Websocket channel consumer for request tunnel.
    """

    def receive(self, text_data=None, bytes_data=None):
        """
        On receive callback to process received event.
        This will validate the request to join a group
        authentication and process accordingly.

        :param text_data: A str of a json even object
        :param bytes_data: *
        :return: None
        """
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
        """
        Send an event to a specific group.

        :param event: a Str containing a dict object to send.
        :return: None
        """
        self.send(
            text_data=json.dumps(
                {"type": event["data"]["type"], "content": event["data"]["message"]}
            )
        )
