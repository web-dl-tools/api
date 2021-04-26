"""
Download handlers.

This file contains custom objects for the BaseHandler and BaseHandlerStatus.
Custom handlers must at a minimum implement the BaseHandler.
"""
from sentry_sdk import capture_exception

from .models import BaseRequest
from .loggers import BaseLogger
from .tasks import delete_request_files


class BaseHandlerStatus(object):
    """
    A base handler status object which is used to enforce a fixed status response
    when retrieving support status from all registered handlers.
    """

    request = None
    supported = False
    options = {}

    def __init__(self, request: str, supported=False, options=dict) -> None:
        """
        Initialize the handler status object.

        :param request: A BaseRequest object to notify the BaseRequest the status belongs to.
        :param supported: An optional bool for the handler supported status.
        :param options: An optional dict containing custom options the handler may support/require.
        """
        self.request = request
        self.supported = supported
        self.options = options

        super().__init__()

    def set_supported(self, supported: bool) -> None:
        """
        Set supported status.

        :param supported: A bool for the handler supported status.
        :return: None
        """
        self.supported = supported

    def set_options(self, options: dict) -> None:
        """
        Set options.

        :param options: A dict containing custom options the handler may support/require.
        :return: None
        """
        self.options = options

    def get_status(self) -> dict:
        """
        get the handler status.

        :return: A dict containing an enforced handler status.
        """
        return {
            "request": self.request,
            "supported": self.supported,
            "options": self.options,
        }


class BaseHandler(object):
    """
    an abstract base handler which processing a base download request and
    automatically updates the status and linked logs.

    In it's current state it immediately completes a request without performing any commands.
    When implemented _action function can be extended where needed.
    """

    request = None
    logger = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        raise NotImplementedError("Child handler must implement handles() function.")

    def __init__(self, request: BaseRequest) -> None:
        """
        Initialize the handler object with an associated request.

        :param request: A BaseRequest containing the request options.
        :return: None
        """
        self.request = request
        self.logger = BaseLogger(
            self.request,
            f"logger.{self.request.get_handler_object().__name__}.{self.request.id}",
        )

        super().__init__()

    def handle(self) -> None:
        """
        Traverse through the _action methods and possibly trigger a full reset.

        :return: None
        """
        try:
            self._pre_process()
            self._download()
            self._post_process()
            self._complete()
        except Exception as e:
            self.logger.error(str(e))
            capture_exception(e)
            self._reset()

    def _pre_process(self) -> None:
        """
        Pre process the request by setting the request status to PRE_PROCESSING.
        Do not overwrite or extend this method. Instead implement the pre_process() method to add additional steps.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_PRE_PROCESSING)
        self.pre_process()

    def pre_process(self) -> None:
        """
        (Optionally) perform additional pre processing steps before continuing.

        :return: None
        """
        pass

    def _download(self) -> None:
        """
        Download the request by setting the request status to DOWNLOADING.
        Do not overwrite or extend this method. Instead implement the download() method to add additional steps.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_DOWNLOADING)
        self.download()

    def download(self) -> None:
        """
        (Optionally) perform additional download steps before continuing.

        :return: None
        """
        pass

    def _post_process(self) -> None:
        """
        Post process the request by setting the request status to POST_PROCESSING.
        Do not overwrite or extend this method. Instead implement the post_process() method to add additional steps.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_POST_PROCESSING)
        self.post_process()

    def post_process(self) -> None:
        """
        (Optionally) perform additional post processing steps before continuing.

        :return: None
        """
        pass

    def _complete(self) -> None:
        """
        Complete the request by setting the request status to COMPLETED.
        Do not overwrite or extend this method. Instead implement the complete() method to add additional steps.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_COMPLETED)
        self.complete()

    def complete(self) -> None:
        """
        (Optionally) perform additional complete steps before continuing.

        :return: None
        """
        pass

    def _reset(self) -> None:
        """
        Reset the handler, sets the request status to FAILED and clears all previously generated files.
        Do not overwrite or extend this method. Instead implement the reset() method to add additional steps.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_FAILED)
        self.request.set_progress(0)
        self.request.set_title("")
        self.request.set_data({})

        self.reset()

        delete_request_files.delay(self.request.path)

    def reset(self) -> None:
        """
        (Optionally) perform additional reset steps before continuing.

        :return: None
        """
        pass
