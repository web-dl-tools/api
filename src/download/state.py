"""
Download state.

This file contains the model object definitions for the request state.
"""
from src.download.exceptions import BaseRequestSetStatusException
from src.download.models import BaseRequest


class BaseRequestState(object):
    """
    an abstract base request state which describes possible state change options.

    In it's current state it denies all state changes.
    When implemented state change _function can be extended to allow a state change.
    """

    request = None

    def __init__(self, request: BaseRequest) -> None:
        """
        Initialize the request state object.

        :param request: A BaseRequest object to notify the BaseRequest the status on status changes.
        """
        self.request = request
        print(self.__class__)

        super().__init__()

    def pending(self) -> None:
        """
        Switch the request state to a pending state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_PENDING}"
        )

    def pre_processing(self) -> None:
        """
        Switch the request state to a pre processing state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_PRE_PROCESSING}"
        )

    def downloading(self) -> None:
        """
        Switch the request state to a downloading state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_DOWNLOADING}"
        )

    def post_processing(self) -> None:
        """
        Switch the request state to a post processing state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_POST_PROCESSING}"
        )

    def completed(self) -> None:
        """
        Switch the request state to a completed state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_COMPLETED}"
        )

    def failed(self) -> None:
        """
        Switch the request state to a failed state.

        :return: None
        """
        raise BaseRequestSetStatusException(
            f"Request state change isn't supported. (from {self.request.status} to {BaseRequest.STATUS_FAILED}"
        )


class PendingRequestState(BaseRequestState):
    """
    An pending request state object.
    """

    def pre_processing(self) -> None: self.request.set_status(BaseRequest.STATUS_PRE_PROCESSING)
    def failed(self) -> None: self.request.set_status(BaseRequest.STATUS_FAILED)


class PreProcessingRequestState(BaseRequestState):
    """
    An pre processing request state object.
    """

    def downloading(self) -> None: self.request.set_status(BaseRequest.STATUS_DOWNLOADING)
    def failed(self) -> None: self.request.set_status(BaseRequest.STATUS_FAILED)


class DownloadingRequestState(BaseRequestState):
    """
    An downloading request state object.
    """

    def post_processing(self) -> None: self.request.set_status(BaseRequest.STATUS_POST_PROCESSING)
    def failed(self) -> None: self.request.set_status(BaseRequest.STATUS_FAILED)


class PostProcessingRequestState(BaseRequestState):
    """
    An post processing request state object.
    """

    def post_processing(self) -> None: return   # Support early post processing triggers.
    def completed(self) -> None: self.request.set_status(BaseRequest.STATUS_COMPLETED)
    def failed(self) -> None: self.request.set_status(BaseRequest.STATUS_FAILED)


class CompletedRequestState(BaseRequestState):
    """
    An completed request state object.
    """

    pass


class FailedRequestState(BaseRequestState):
    """
    An failed request state object.
    """

    def pending(self) -> None: self.request.set_status(BaseRequest.STATUS_PENDING)
