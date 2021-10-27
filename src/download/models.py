"""
Download models.

This file contains the model object definitions for the polymorphic BaseRequest and custom Log object.
"""
import abc

from typing import Type
from polymorphic.models import PolymorphicModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from src.db.models import IdMixin, CreatedAtMixin, ModifiedAtMixin
from .exceptions import BaseRequestSetProgressException


class BaseRequest(ModifiedAtMixin, CreatedAtMixin, IdMixin, PolymorphicModel):
    """
    A concrete polymorphic base request model which can be implemented to extend it with custom handler specific fields.
    Due to the polymorphic nature of this model a relationship is automatically added between the parent-child models.
    """

    STATUS_PENDING = "pending"
    STATUS_PRE_PROCESSING = "pre_processing"
    STATUS_DOWNLOADING = "downloading"
    STATUS_POST_PROCESSING = "post_processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUSES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PRE_PROCESSING, "Pre processing"),
        (STATUS_DOWNLOADING, "Downloading"),
        (STATUS_POST_PROCESSING, "Post processing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    status = models.CharField(
        _("status"), max_length=15, choices=STATUSES, default=STATUS_PENDING
    )
    url = models.TextField(_("url"))
    start_processing_at = models.DateTimeField(_("start processing at"), null=True)
    completed_at = models.DateTimeField(_("completed at"), null=True)
    start_compressing_at = models.DateTimeField(_("start compressing at"), null=True)
    compressed_at = models.DateTimeField(_("compressed at"), null=True)
    progress = models.IntegerField(_("progress"), default=0)
    title = models.CharField(_("title"), max_length=200, blank=True)
    data = models.JSONField(_("data"), default=dict)

    class Meta:
        """
        Model metadata.
        See https://docs.djangoproject.com/en/3.0/ref/models/options/
        """

        db_table = "base_request"

    def get_state(self) -> "src.download.state.BaseRequestState":
        """
        Get the state object for the current request state.

        :return: BaseRequestState
        """
        from .state import PendingRequestState, PreProcessingRequestState, DownloadingRequestState, \
            PostProcessingRequestState, CompletedRequestState, FailedRequestState

        if self.status == self.STATUS_PENDING: return PendingRequestState(self)
        elif self.status == self.STATUS_PRE_PROCESSING: return PreProcessingRequestState(self)
        elif self.status == self.STATUS_DOWNLOADING: return DownloadingRequestState(self)
        elif self.status == self.STATUS_POST_PROCESSING: return PostProcessingRequestState(self)
        elif self.status == self.STATUS_COMPLETED: return CompletedRequestState(self)
        return FailedRequestState(self)

    def set_status(self, status: str) -> None:
        """
        Set the status of the request. Use the state model to verify and enforce state changes.

        :param status: A str containing a (hopefully) valid status.
        :return: None
        """
        self.status = status
        update_fields = ["status"]

        if status == self.STATUS_PRE_PROCESSING:
            self.start_processing_at = timezone.now()
            update_fields.append("start_processing_at")
        elif status == self.STATUS_COMPLETED:
            self.completed_at = timezone.now()
            update_fields.append("completed_at")

        async_to_sync(get_channel_layer().group_send)(
            f"requests.group.{self.user.id}",
            {
                "type": "websocket.send",
                "data": {
                    "type": "requests.status.update",
                    "message": {
                        "id": str(self.id),
                        "status": self.status
                    },
                },
            },
        )

        self.save(update_fields=update_fields)

    def set_progress(self, progress: int) -> None:
        """
        Set the progress of the request.

        :param progress: An integer containing the current progress.
        :return: None
        """
        if progress != 0 and self.progress > progress:
            raise BaseRequestSetProgressException(
                f"Progress state change to {progress} is lower than current progress state {self.progress}."
            )
        self.progress = progress
        self.save(update_fields=["progress"])

    def set_start_compressing_at(self, clear = False) -> None:
        """
        Set the start_compressing_at on the current date.

        :param clear: An boolean on whether to clear the field.
        :return: None
        """
        self.start_compressing_at = None if clear else timezone.now()
        self.save(update_fields=["start_compressing_at"])

    def set_compressed_at(self) -> None:
        """
        Set the compressed_at on the current date.

        :return: None
        """
        self.compressed_at = timezone.now()
        self.save(update_fields=["compressed_at"])

    def set_title(self, title: str) -> None:
        """
        Set the title of the request.

        :param title: A str of the request title.
        :return: None
        """
        self.title = title
        self.save(update_fields=["title"])

    def set_data(self, data: dict) -> None:
        """
        Set the data payload field.

        :param data: An dict of handler data.
        :return: None
        """
        self.data = data
        self.save(update_fields=["data"])

    @property
    def path(self) -> str:
        """
        Get the associated relative folder path for storing files when handling the request.

        :return: a str containing a relative custom file path for the current request.
        """
        return f"files/{self.user.id}/{self.id}"

    def get_handler(self) -> "src.download.handlers.BaseHandler":
        """
        Initialize the associated handler with the current request and return it.

        :return: BaseHandler
        """
        return self.get_handler_object()(self)

    @property
    def storage_size(self) -> int:
        """
        Calculate the total request storage size.

        :return: The total storage size.
        """
        from .utils import calculate_storage
        return calculate_storage(self.path)

    @staticmethod
    @abc.abstractmethod
    def get_handler_object() -> "Type[src.download.handlers.BaseHandler]":
        """
        Return the type of the associated handler. This method is called when retrieving
        the type of the associated handler object in order to perform a static function call.

        :return: a Type[BaseHandler] of the BaseHandler object.
        """
        pass


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
        (LEVEL_CRITICAL, "Critical"),
        (LEVEL_FATAL, "Fatal"),
        (LEVEL_ERROR, "Error"),
        (LEVEL_WARNING, "Warning"),
        (LEVEL_WARN, "Warn"),
        (LEVEL_INFO, "Info"),
        (LEVEL_DEBUG, "Debug"),
        (LEVEL_NOTSET, ""),
    )

    request = models.ForeignKey(
        BaseRequest, verbose_name=_("request"), on_delete=models.CASCADE
    )
    level = models.IntegerField(_("level"), choices=LEVELS, default=LEVEL_NOTSET)
    message = models.TextField(_("message"), blank=False)

    @property
    def level_display(self) -> str:
        """
        Get the level display value.

        :return: A str containing the status display value.
        """
        return self.get_level_display()
