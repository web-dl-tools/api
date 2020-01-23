"""
Download handlers.
"""
from .models import BaseRequest


class BaseHandler(object):
    """
    Abstract base handler.
    """
    request = None

    @staticmethod
    def handles(url: str) -> bool:
        """
        Notify if the given url can be handled by the handler.

        :param url: str
        :return: bool
        """
        raise NotImplementedError('Child handler must implement handles() function.')

    def __init__(self, request: BaseRequest) -> None:
        """
        Initialize the handler.

        :param request: BaseRequest
        """
        self.request = request

        super().__init__()

    def handle(self) -> bool:
        """
        Handle the request.

        :return: bool
        """
        try:
            self._pre_process()
            self._process()
            self._post_process()
            self._complete()
            return True
        except Exception as e:
            self._reset()
            print(e)
            return False

    def _pre_process(self) -> None:
        """
        Pre process the request.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_PRE_PROCESSING)

    def _process(self) -> None:
        """
        Process the request.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_DOWNLOADING)

    def _post_process(self) -> None:
        """
        Post process the request results.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_POST_PROCESSING)

    def _complete(self) -> None:
        """
        Complete the request.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_COMPLETED)

    def _reset(self) -> None:
        """
        Reset the handler and clear previously generated files.

        :return: None
        """
        self.request.set_status(BaseRequest.STATUS_FAILED)
