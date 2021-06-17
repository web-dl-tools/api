"""
User utils.

This file contains functions and action not fit for standard Django files.
"""
from src.download.models import BaseRequest


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
