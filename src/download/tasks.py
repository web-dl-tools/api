"""
Download tasks.
"""
import uuid

from config.celery import app
from .models import BaseRequest
from .serializers import PolymorphicRequestSerializer


@app.task
def handle_request(request_id: uuid) -> None:
    """
    Handle the request.

    :return: bool
    """
    request = BaseRequest.objects.get(id=request_id)
    request.get_handler().handle()


def get_handlers(url: str) -> list:
    """
    Get a list of all handlers' status and options.

    :param url: str
    :return: list
    """
    handlers = []
    for a in PolymorphicRequestSerializer.model_serializer_mapping:
        if a is not BaseRequest:
            handlers.append(a.get_handler_object().handles(url).get_status())
    return handlers
