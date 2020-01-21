"""
User views.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class AuthenticateView(ObtainAuthToken):
    """
    Authenticate a user view.
    """
    pass


class GetCurrentUserView(APIView):
    """
    Get current user view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        """
        GET request for retrieving the current user.

        :param args: *
        :param kwargs: *
        :return: Response 200 OK.
        """
        return Response(status=200, data=UserSerializer(self.request.user).data)
