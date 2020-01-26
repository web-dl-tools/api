"""
User views.

This file contains a viewset for the custom User model object and associated Serializer.
"""
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        if self.action == 'create':
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
