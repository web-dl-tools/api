"""
User middleware.

This file contains custom user middlewares.
"""
from channels.http import AsgiRequest
from rest_framework.authtoken.models import Token

from .models import Log


class UserMiddleware(object):
    """
    A middleware for logging user actions.
    """

    def __init__(self, get_response):
        """
        One-time configuration and initialization.

        :param get_response: *
        """
        self.get_response = get_response

    def __call__(self, request: AsgiRequest):
        """
        Log each authenticated request before
        the view (and later middleware(s)) are called.

        :param request: AsgiRequest
        :return: AsgiRequest
        """
        if 'Authorization' in request.headers:
            try:
                user = Token.objects.get(key=request.headers['Authorization'].replace("Token ", "")).user
                Log.objects.create(
                    user=user,
                    url=request.get_full_path(),
                    method=request.method,
                    data=request.body.decode("utf-8") if request.body else None
                )
            except Token.DoesNotExist:
                pass

        return self.get_response(request)
