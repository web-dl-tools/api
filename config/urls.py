"""
config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.application import urls as application_urls
from src.user import urls as user_urls
from src.handlers import urls as handler_urls
from src.download import urls as download_urls

from src.user.views import UserViewSet
from src.download.views import RequestViewSet

router = DefaultRouter(trailing_slash=False)

router.register("users", UserViewSet)
router.register("requests", RequestViewSet)

urlpatterns = [
    path("admin", admin.site.urls),
    path("api/application/", include(application_urls)),
    path("api/users/", include(user_urls)),
    path("api/handlers/", include(handler_urls)),
    path("api/download/", include(download_urls)),
    path("api/", include(router.urls)),
]
