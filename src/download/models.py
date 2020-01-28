"""
Download models.

This file contains the model object definitions for the polymorphic BaseRequest and custom Log object.
"""
from typing import Type
from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from src.db.models import IdMixin, CreatedAtMixin, ModifiedAtMixin
from .exceptions import BaseRequestSetStatusException


class BaseRequest(ModifiedAtMixin, CreatedAtMixin, IdMixin, PolymorphicModel):
    """
    A concrete polymorphic base request model which can be implemented to extend it with custom handler specific fields.
    Due to the polymorphic nature of this model a relationship is automatically added between the parent-child models.
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
    data = JSONField(_('data'), default=dict)

    class Meta:
        """
        Model metadata.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """
        db_table = 'base_request'

    def set_status(self, status: str) -> None:
        """
        Set the status of the request after validating the given status and status change from the current status.

        :param status: A str containing a (hopefully) valid status.
        :return: None
        """
        if status == self.status:
            return
        elif self.status == self.STATUS_COMPLETED:
            raise BaseRequestSetStatusException(f"Request has already completed.")
        elif (status == self.STATUS_FAILED) or \
             (self.status == self.STATUS_FAILED and status == self.STATUS_PENDING) or \
             (self.status == self.STATUS_PENDING and status == self.STATUS_PRE_PROCESSING) or \
             (self.status == self.STATUS_PRE_PROCESSING and status == self.STATUS_DOWNLOADING) or \
             (self.status == self.STATUS_DOWNLOADING and status == self.STATUS_POST_PROCESSING) or \
             (self.status == self.STATUS_POST_PROCESSING and status == self.STATUS_COMPLETED):
            self.status = status
            self.save(update_fields=['status'])
        elif status in (s[0] for s in self.STATUSES):
            raise BaseRequestSetStatusException(
                f"Status state change to {status} is nog possible from current status state {self.state}.")
        else:
            raise BaseRequestSetStatusException(f"Status {status} is not supported.")

    def set_data(self, data: dict) -> None:
        """
        Set the data payload field.

        :param data: An dict of handler data.
        :return: None
        """
        self.data = data
        self.save(update_fields=['data'])

    @property
    def path(self) -> str:
        """
        Get the associated relative folder path for storing files when handling the request.

        :return: a str containing a relative custom file path for the current request.
        """
        return f'files/{self.user.id}/{self.id}'

    def get_handler(self) -> 'src.download.handlers.BaseHandler':
        """
        Initialize the associated handler with the current request and return it.

        :return: BaseHandler
        """
        return self.get_handler_object()(self)

    @staticmethod
    def get_handler_object() -> 'Type[src.download.handlers.BaseHandler]':
        """
        Return the type of the associated handler. This method is called when retrieving
        the type of the associated handler object in order to perform a static function call.

        :return: a Type[BaseHandler] of the BaseHandler object.
        """
        raise NotImplementedError('Child request must implement get_handler() function.')


class Log(CreatedAtMixin, IdMixin):
    """
    A request log model object for storing logging data from the associated BaseHandler when handling the request.
    """
    LEVEL_CRITICAL = 50
    LEVEL_FATAL = LEVEL_CRITICAL
    LEVEL_ERROR = 40
    LEVEL_WARNING = 30
    LEVEL_WARN = LEVEL_WARNING
    LEVEL_INFO = 20
    LEVEL_DEBUG = 10
    LEVEL_NOTSET = 0

    LEVELS = (
        (LEVEL_CRITICAL, 'Critical'),
        (LEVEL_FATAL, 'Fatal'),
        (LEVEL_ERROR, 'Error'),
        (LEVEL_WARNING, 'Warning'),
        (LEVEL_WARN, 'Warn'),
        (LEVEL_INFO, 'Info'),
        (LEVEL_DEBUG, 'Debug'),
        (LEVEL_NOTSET, ''),
    )

    request = models.ForeignKey(BaseRequest, verbose_name=_('request'), on_delete=models.CASCADE)
    level = models.IntegerField(_('level'), choices=LEVELS, default=LEVEL_NOTSET)
    message = models.TextField(_('message'), blank=False)
