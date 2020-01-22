"""
Download models.
"""
from django.db import models

from src.db.models import IdMixin, TimestampMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Request(TimestampMixin, IdMixin, models.Model):
    """
    Concrete base request model.
    """
    STATUS_PENDING = 'pending'
    STATUS_PRE_PROCESSING = 'pre_processing'
    STATUS_DOWNLOADING = 'downloading'
    STATUS_POST_PROCESSING = 'post_processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUSES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PRE_PROCESSING, 'Pre processing'),
        (STATUS_DOWNLOADING, 'Downloading'),
        (STATUS_POST_PROCESSING, 'Post processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    status = models.CharField(_('status'), max_length=15, choices=STATUSES, default=STATUS_PENDING)
    url = models.URLField(_('url'))

    def get_handler(self) -> 'src.download.handlers.BaseHandler':
        """
        Get the handler for the request.

        :return: BaseHandler
        """
        raise NotImplementedError('Child request must implement get_handler() function.')

    def get_name(self) -> str:
        """
        Get the handler verbose/url name.

        :return: str
        """
        raise NotImplementedError('Child request must implement get_name() function.')