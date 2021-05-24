"""
Download tasks.

This file contains commonly used tasks and Celery tasks for asynchronous task handling.
"""
import os
import uuid
import shutil

from config.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import BaseRequest


@app.task
def compress_request(request_id: uuid) -> None:
    """
    Compress request file contents.

    :param request_id: a UUID4 containing the id of a valid BaseRequest.
    :return: None.
    """
    request = BaseRequest.objects.get(id=request_id)

    if not os.path.exists(request.path):
        request.set_start_compressing_at(True)
        return

    request.set_start_compressing_at()
    if not os.path.isfile(f'{request.path}.zip'):
        shutil.make_archive(request.path, 'zip', request.path)
    request.set_compressed_at()

    async_to_sync(get_channel_layer().group_send)(
        f"requests.group.{request.user.id}",
        {
            "type": "websocket.send",
            "data": {
                "type": "requests.task.finished",
                "message": {
                    "id": str(request_id),
                    "task": 'compress_request'
                },
            },
        },
    )


@app.task
def download_request(request_id: uuid) -> None:
    """
    Handle a given BaseRequest in a asynchronous task queue.
    The BaseRequest is retrieved in task instead of given as a request param in order to ensure
    no model mutations have been made and prevent conflicts.

    :param request_id: a UUID4 containing the id of a valid BaseRequest.
    :return: None
    """
    request = BaseRequest.objects.get(id=request_id)
    request.get_handler().handle()


@app.task
def delete_request_files(path: str) -> None:
    """
    Removed the associated files (if any) from an already deleted request.

    :param path: a str containing the request files folder path.
    :return: None
    """
    shutil.rmtree(path, ignore_errors=True)
    if os.path.isfile(f'{path}.zip'):
        os.remove(f'{path}.zip')
