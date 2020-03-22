"""
Resource handlers.

This file contains the BaseHandler implementation of the resource handler.
"""
import requests

from src.download.handlers import BaseHandler, BaseHandlerStatus


class ResourceHandler(BaseHandler):
    """
    A resource handler which implements the BaseHandler object.
    """

    extension = None
    filename = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        from .models import ResourceRequest

        status = BaseHandlerStatus(ResourceRequest.__name__)
        status.set_description("A handler for downloading resources from the url resource.")
        status.set_options({})

        try:
            r = requests.head(url, allow_redirects=True)
            status.set_supported(r.status_code == 200)
        except requests.exceptions.InvalidSchema:
            status.set_supported(False)

        return status

    def _pre_process(self) -> None:
        """
        An extension of the _pre_process method which
        .

        :return: None
        """
        super()._pre_process()
        raise Exception('for development purposes.')


    def _download(self) -> None:
        """
        An extension of the _download method which
        .

        :return: None
        """
        super()._download()

