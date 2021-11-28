"""
User views.

This file contains a viewset for the custom User model object and associated Serializer.
"""
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import User, Log
from .serializers import UserSerializer, LogSerializer
from .utils import parse_requests_storage


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    A view set for authenticating and viewing a user instances.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self) -> list:
        """
        Instantiates and returns the list of permissions that the given requires.
        This allows us to use the create method without any authentication while
        enforcing authentication for the other endpoints in the viewset.

        :return: a list containing permission class objects for a given action.
        """
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        """
        Get the currently authenticated user.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: Response
        """
        return Response(status=200, data=UserSerializer(self.request.user).data)

    @action(detail=False, url_path='me/logs')
    def logs(self, request, *args, **kwargs):
        """
        Get the currently authenticated user's logs.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: Response
        """
        dt = timezone.localtime()
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        return Response(status=200, data=LogSerializer(
            Log.objects.filter(user=request.user, created_at__gte=start).order_by('-created_at'), many=True
        ).data)

    @action(detail=False, url_path='me/storage')
    def storage(self, request, *args, **kwargs):
        """
        Get the currently authenticated user's logs.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: Response
        """
        return JsonResponse(parse_requests_storage(request.user), safe=False)

    def update(self, request, *args, **kwargs):
        """
        Check if the authentication user is editing itself.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: Response
        """
        if self.request.user != self.get_object():
            return Response(status=401, data="Unauthorized request")

        return super().update(request, *args, **kwargs)
