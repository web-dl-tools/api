"""
User urls.
"""
from django.urls import path

from .views import GetCurrentUserView, AuthenticateView


urlpatterns = [
    path('authenticate', AuthenticateView.as_view()),
    path('me', GetCurrentUserView.as_view()),
]
