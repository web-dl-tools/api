"""
User views.
"""
import re

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .tasks import get_handlers


class GethandlerStatusesView(APIView):
    """
    An APIView for retrieving all handler options and support statuses.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        """
        Traverse all handlers to retrieve handler options and support status.

        :param args: *
        :param kwargs: *
        :return: Response
        """
        url = self.request.query_params.get("url")
        regexp = re.compile(
            r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        )
        return (
            Response(status=200, data=get_handlers(url))
            if url and regexp.search(url)
            else Response(status=400)
        )
