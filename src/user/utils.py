"""
User utils.

This file contains functions and action not fit for standard Django files.
"""
from rest_framework.exceptions import AuthenticationFailed

from src.download.models import BaseRequest
from .models import User


def parse_requests_storage(user: str) -> list:
    """
    Parse the user requests storage.

    :param user: The user to parse requests for
    :return: A list containing each request and storage data
    """
    storage = []

    requests = BaseRequest.objects.filter(user=user)
    for request in requests:
        storage.append({
            'id': str(request.id),
            'title': request.title,
            'type': str(request.polymorphic_ctype.model),
            'size': request.storage_size
        })

    return storage

def update_password(user: User, current_password: str, new_password: str) -> None:
    """
    Check passwords and update the password for the a user.

    :param user: The user to check and update with/for
    :param current_password: The current password
    :param new_password: The new password
    :return: None
    """
    if not user.check_password(current_password):
        raise AuthenticationFailed('Invalid current password')

    user.set_password(new_password)
    user.save(update_fields=["password"])
