"""
Celery config.
"""
import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery('api')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
