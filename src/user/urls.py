"""
User urls.
"""
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('authenticate/', ObtainAuthToken.as_view()),
]
