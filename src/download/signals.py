"""
Download signals.

This file contains handler functions for DB signals send by Django when performing ORM actions.
"""
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from channels.layers import get_channel_layer
from django.utils import timezone
from asgiref.sync import async_to_sync

from .models import BaseRequest
from .tasks import download_request, delete_request_files
from .serializers import PolymorphicRequestSerializer


@receiver(pre_save)
def my_callback(sender, instance, *args, **kwargs):
    """
    Automatically update the modified at field to the current datetime whenever
    the request entity is modified.

    :param sender: models.Model object which triggered the save action.
    :param instance: a BaseRequest instance.
    """
    instance.modified_at = timezone.now()


@receiver(post_save)
def handle_request_post_save(sender, instance, created, **kwargs) -> None:
    """
    Automatically handle a BaseRequest object, after it has been created, in a asynchronous task queue.
    Additionally this triggers a websocket send event to a authenticated group in order to notify members
    of the request data change.

    :param sender: models.Model object which triggered the save action.
    :param instance: a BaseRequest instance.
    :param created: a bool whether the object is newly created.
    :param kwargs: *
    :return: None
    """
    if isinstance(instance, BaseRequest):
        if created:
            download_request.delay(instance.id)
        else:
            async_to_sync(get_channel_layer().group_send)(
                f"requests.group.{instance.user.id}",
                {
                    "type": "websocket.send",
                    "data": {
                        "type": "requests.update",
                        "message": PolymorphicRequestSerializer(instance=instance).data,
                    },
                },
            )


@receiver(pre_delete)
def handle_request_post_delete(sender, instance, using, **kwargs) -> None:
    """
    Automatically delete request files, before it will be deleted, in a asynchronous task queue.

    :param sender: models.Model object which triggered the save action.
    :param instance: a BaseRequest instance.
    :param using: The database instance being used.
    :param kwargs: *
    :return: None
    :return:
    """
    if isinstance(instance, BaseRequest):
        delete_request_files.delay(instance.path)
