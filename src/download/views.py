"""
Download views.
"""
import re

from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import BaseRequest
from .serializers import PolymorphicRequestSerializer, LogSerializer
from .tasks import handle_request, get_handlers


class RequestViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A view set for creating, viewing and retrying Request instances.
    """
    queryset = BaseRequest.objects.all()
    serializer_class = PolymorphicRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self) -> QuerySet:
        """
        Filter the queryset based on the user, so that it can only view it's own requests.

        :return: QuerySet
        """
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=False)
    def handlers(self, request, *args, **kwargs):
        """
        Traverse all handlers to retrieve handler options and support status.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: Response
        """
        url = self.request.query_params.get('url')
        regexp = re.compile(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        return Response(status=200, data=get_handlers(url)) if url and regexp.search(url) else Response(status=400)

    def create(self, request, *args, **kwargs):
        """
        Create a Request and add the user from the request to the payload.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: *
        """
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=True)
    def logs(self, request, pk=None) -> Response:
        """
        Get request logs.

        :param request: Request
        :param pk: str
        :return: Response
        """
        request = self.get_object()
        return Response(LogSerializer(request.log_set, many=True).data)

    @action(detail=True, methods=['PUT'])
    def retry(self, request, pk=None) -> Response:
        """
        Retry a failed request.

        :param request: *
        :param pk: str
        :return: Response
        """
        request = self.get_object()
        serializer = self.get_serializer(request)
        if request.status != BaseRequest.STATUS_FAILED:
            return Response(status=400)
        else:
            request.set_status(BaseRequest.STATUS_PENDING)
            handle_request.delay(request.id)
            return Response(serializer.data)
