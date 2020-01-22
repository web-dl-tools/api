"""
Download handlers.
"""


class BaseHandler(object):
    """
    Abstract base handler.
    """
    def get_request_model(self) -> 'src.download.models.Request':
        """
        Get the request model associated with the handler.

        :return: Request
        """
        raise NotImplementedError('Child handler must implement get_request_model() function.')

    def handles(self, url: str) -> bool:
        """
        Notify if the given url can be handled by the handler.

        :param url: str
        :return: bool
        """
        raise NotImplementedError('Child handler must implement handles() function.')
