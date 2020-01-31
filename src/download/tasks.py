"""
Download tasks.

This file contains commonly used tasks and Celery tasks for asynchronous task handling.
"""
import uuid

from config.celery import app
from .models import BaseRequest


@app.task
def handle_request(request_id: uuid) -> None:
    """
    Handle a given BaseRequest in a asynchronous task queue.
    The BaseRequest is retrieved in task instead of given as a request param in order to ensure
    no model mutations have been made and prevent conflicts.

    :param request_id: a UUID4 containing the id of a valid BaseRequest.
    :return: None
    """
    request = BaseRequest.objects.get(id=request_id)
    request.get_handler().handle()
