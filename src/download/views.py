"""
Download views.
"""
from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import BaseRequest
from .serializers import PolymorphicRequestSerializer, LogSerializer


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
