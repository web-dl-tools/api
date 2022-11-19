"""
Application views.

This file contains the views for the custom application endpoints.
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .utils import get_build_info


@api_view(['GET'])
def build_info(_):
    """
    Return information about the current build of the API.
    """
    return JsonResponse(get_build_info())
