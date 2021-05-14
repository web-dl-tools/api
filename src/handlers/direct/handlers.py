"""
Direct handlers.

This file contains the BaseHandler implementation of the direct handler.
"""
import requests

from src.download.handlers import BaseHandler, BaseHandlerStatus
from ..utils import create_resource_folder, extract_file_extension, extract_filename, download_request


class DirectHandler(BaseHandler):
    """
    A direct handler which implements the BaseHandler object.
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
        from .models import DirectRequest

        status = BaseHandlerStatus(DirectRequest.__name__)
        status.set_options({})

        try:
            r = requests.head(url, allow_redirects=True)
            status.set_supported(r.status_code == requests.codes.ok)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema):
            status.set_supported(False)

        return status

    def pre_process(self) -> None:
        """
        Additional pre-processing steps which
        prepares the filepath and retrieves file props.

        :return: None
        """
        r = requests.head(self.request.url, allow_redirects=True)
        self.request.set_data(dict(r.headers))
        self.logger.debug("Retrieved header information.")

        self.extension = extract_file_extension(dict(r.headers))
        self.filename = extract_filename(self.request.url, dict(r.headers), self.extension)
        self.request.set_title(self.filename)
        self.logger.debug(
            f"Extracted extension {self.extension} and filename/title {self.filename}."
        )

        create_resource_folder(self.request.path)
        self.logger.debug(f"Created folder for resource.")

    def download(self) -> None:
        """
        Additional download steps which
        download the direct request using requests.

        :return: None
        """
        def progress_cb(progress: int) -> None:
            if progress > self.request.progress:
                self.request.set_progress(progress)

        self.logger.debug(f"Started download for {self.request.url}.")
        result = download_request(self.request.url, self.request.path, self.filename, self.extension, progress_cb)

        if result.get("success"):
            self.logger.info(f"Finished download with {', '.join('{} {}'.format(k,v) for k,v in result.items())}.")
        else:
            self.logger.error(f"Failed download with {', '.join('{} {}'.format(k,v) for k,v in result.items())}.")
