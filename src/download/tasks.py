import uuid

from .models import BaseRequest


def handle_request(request_id: uuid) -> None:
    """
    Handle the request.

    :return: bool
    """
    request = BaseRequest.objects.get(id=request_id)
    request.get_handler().handle()
