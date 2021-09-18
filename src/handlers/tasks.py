"""
Handlers tasks.

This file contains commonly used tasks.
"""
from src.download.serializers import PolymorphicRequestSerializer
from src.download.models import BaseRequest


def get_handlers(url: str) -> list:
    """
    Traverse all registered handlers and retrieve handler statuses for all handlers for a given url.

    :param url: a str containing a valid url.
    :return: a list containing all handler status results.
    """
    handlers = []
    for handler in PolymorphicRequestSerializer.model_serializer_mapping:
        if handler is not BaseRequest:
            handlers.append(handler.get_handler_object().handles(url).get_status())
    return handlers
