"""
Application views.

This file contains the views for the custom application endpoints.
"""
from django.http import JsonResponse
from .utils import get_build_info

def build_info(request):
    """
    Return information about the current build of the API.
    """
    return JsonResponse(get_build_info())
