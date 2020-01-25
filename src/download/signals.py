"""
Download signals.
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import BaseRequest
from .tasks import handle_request as handle_request_task


@receiver(post_save)
def handle_request(sender, instance, created, **kwargs) -> None:
    """
    Handle the request after it has been created.

    :param sender: *
    :param instance: BaseRequest
    :param created: bool
    :param kwargs: *
    :return: None
    """
    if isinstance(instance, BaseRequest) and created:
        handle_request_task.delay(instance.id)
