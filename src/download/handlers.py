"""
Download handlers.

This file contains custom objects for the BaseHandler and BaseHandlerStatus.
Custom handlers must at a minimum implement the BaseHandler.
"""
from .models import BaseRequest
from .loggers import BaseLogger


class BaseHandlerStatus(object):
    """
    A base handler status object which is used to enforce a fixed status response
    when retrieving support status from all registered handlers.
    """

    request = None
    description = ""
    supported = False
    options = {}

    def __init__(
        self, request: str, description=str, supported=False, options=dict
    ) -> None:
        """
        Initialize the handler status object.

        :param request: A BaseRequest object to notify the BaseRequest the status belongs to.
        :param description: A str to describe the handler.
        :param supported: An optional bool for the handler supported status.
        :param options: An optional dict containing custom options the handler may support/require.
        """
        self.request = request
        self.description = description
        self.supported = supported
        self.options = options

        super().__init__()

    def set_description(self, description: str) -> None:
        """
        Set the description.

        :param description: A str to describe the handler.
        :return: None
        """
        self.description = description

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
            "description": self.description,
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
            self._reset()
            self.logger.error(str(e))

    def _pre_process(self) -> None:
        """
        Pre process the request by setting the request status to PRE_PROCESSING.
        Handler objects extending this method must call super()._pre_process()
        before continuing with custom handler commands.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_PRE_PROCESSING)

    def _download(self) -> None:
        """
        Download the request by setting the request status to DOWNLOADING.
        Handler objects extending this method must call super()._download()
        before continuing with custom handler commands.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_DOWNLOADING)

    def _post_process(self) -> None:
        """
        Post process the request by setting the request status to POST_PROCESSING.
        Handler objects extending this method must call super()._post_processing()
        before continuing with custom handler commands.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_POST_PROCESSING)

    def _complete(self) -> None:
        """
        Complete the request by setting the request status to COMPLETED.
        Handler objects extending this method must call super()._complete()
        before continuing with custom handler commands.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_COMPLETED)

    def _reset(self) -> None:
        """
        Reset the handler and clears all previously generated files.
        Handler objects extending this method must call super()._reset()
        before continuing with custom handler commands.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_FAILED)
        self.request.set_progress(0)
        self.request.set_title("")
        self.request.set_data({})
