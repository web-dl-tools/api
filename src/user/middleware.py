"""
User middleware.

This file contains custom user middlewares.
"""
from channels.http import AsgiRequest
from rest_framework.authtoken.models import Token

from .models import Log
from .exceptions import SensitiveRequestException


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
        try:
            data = self.scrub_sensitive_data(request)
        except SensitiveRequestException:
            return self.get_response(request)

        auth_token = self.retrieve_auth_token(request)        
 
        if auth_token:
            try:
                user = Token.objects.get(key=auth_token).user
                Log.objects.create(
                    user=user,
                    url=request.get_full_path(),
                    method=request.method,
                    data=data
                )
            except Token.DoesNotExist:
                pass

        return self.get_response(request)

    def scrub_sensitive_data(self, request: AsgiRequest) -> str:
        """
        Scrub sensitive data from the request.

        :param request: AsgiRequest
        :return: str
        """
        request_parts = request.get_full_path().split('/')
        if 'admin' in request_parts[1]:
            raise SensitiveRequestException('Request is an admin request.')
        if request_parts[-1] == 'credentials':
            data = 'Filtered out due to containing sensitive information.'
        else:
            data = request.body.decode("utf-8") if request.body else None
        
        return data

    def retrieve_auth_token(self, request: AsgiRequest) -> str:
        """
        Retrieve the auth token from the request.

        :param request: AsgiRequest
        :return: str
        """
        return request.headers['Authorization'].replace("Token ", "") if 'Authorization' in request.headers else request.COOKIES.get('auth_token')
