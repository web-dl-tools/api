"""
Authentication views.

This file contains the views for the custom authentication endpoints.
"""
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.response import Response
from rest_framework.views import APIView

from src.authentication.authentication import CookieTokenAuthentication
from src.download.utils import list_files, prepare_path, validate_for_request,  validate_for_archive, log_file_access


class VerifyFileAccessView(APIView):
    """
    An API view for checking file access.
    """
    authentication_classes = [CookieTokenAuthentication]

    def get(self, request):
        """
        Validate a nginx subrequest cookie auth token and subsequent file access for the given auth token user.

        :param request: Request
        :return: Response
        """
        user, _ = self.get_authenticators()[0].get_user_by_cookie_auth_token(request)
        path = prepare_path(request.headers.get('X-Original-Uri')[1:])

        is_valid_for_request = validate_for_request(path, user)
        is_valid_for_archive = validate_for_archive(path, user)

        if is_valid_for_request or is_valid_for_archive:
            if is_valid_for_request:
                file_log = log_file_access(path)
                async_to_sync(get_channel_layer().group_send)(
                    f"requests.group.{user.id}",
                    {
                        "type": "websocket.send",
                        "data": {
                            "type": "requests.files.retrieved",
                            "message": json.dumps(list_files(file_log.request.path), default=str),
                        },
                    },
                )
            return Response(status=200)

        return Response(status=403, data="You're not authorized to access this resource or the resource doesn't exist.")
