"""
Download signals.

This file contains handler functions for DB signals send by Django when performing ORM actions.
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import BaseRequest
from .tasks import handle_request as handle_request_task


@receiver(post_save)
def handle_request(sender, instance, created, **kwargs) -> None:
    """
    Automatically handle a BaseRequest object, after it has been created, in a asynchronous task queue.

    :param sender: models.Model object which triggered the save action.
    :param instance: a BaseRequest instance.
    :param created: a bool whether the object is newly created.
    :param kwargs: *
    :return: None
    """
    if isinstance(instance, BaseRequest) and created:
        handle_request_task.delay(instance.id)
