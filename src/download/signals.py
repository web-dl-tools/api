"""
Download signals.

This file contains handler functions for DB signals send by Django when performing ORM actions.
"""
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import BaseRequest
from .tasks import download_request, delete_request_files


@receiver(post_save)
def handle_request_post_save(sender, instance, created, **kwargs) -> None:
    """
    Automatically handle a BaseRequest object, after it has been created, in a asynchronous task queue.

    :param sender: models.Model object which triggered the save action.
    :param instance: a BaseRequest instance.
    :param created: a bool whether the object is newly created.
    :param kwargs: *
    :return: None
    """
    if isinstance(instance, BaseRequest) and created:
        download_request.delay(instance.id)


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
