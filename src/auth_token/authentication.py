from rest_framework.authentication import TokenAuthentication


class CookieTokenAuthentication(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support cookie authentication
    in the form of "auth_token=<token_key>"
    """

    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if (
            "auth_token" in request.COOKIES
            and "HTTP_AUTHORIZATION" not in request.META
        ):
            return self.authenticate_credentials(request.COOKIES.get("auth_token"))
        else:
            return super(CookieTokenAuthentication, self).authenticate(request)
