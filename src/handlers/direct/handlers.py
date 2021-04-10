"""
Direct handlers.

This file contains the BaseHandler implementation of the direct handler.
"""
import os
import re
import requests
import mimetypes

from src.download.handlers import BaseHandler, BaseHandlerStatus


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
        except requests.exceptions.InvalidSchema:
            status.set_supported(False)

        return status

    def pre_process(self) -> None:
        """
        Additional pre-processing steps which
        prepares the filepath and retrieves file props.

        :return: None
        """
        r = requests.head(self.request.url, allow_redirects=True)
        headers = r.headers
        self.request.set_data(dict(headers))
        self.logger.debug("Retrieved header information.")

        content_type = headers["content-type"].split(";")[0]
        self.extension = mimetypes.guess_extension(content_type)
        self.filename = (
            re.findall("filename=(.+)", headers["Content-Disposition"])[0]
            if "Content-Disposition" in headers.keys()
            else self.request.url.split("/")[-1]
        )
        if self.filename.endswith(self.extension):
            self.filename = self.filename[: -len(self.extension)]
        self.request.set_title(self.filename)
        self.logger.debug(
            f"Extracted extension {self.extension} and created filename {self.filename}."
        )

        if not os.path.exists(self.request.path):
            os.makedirs(self.request.path)
            self.logger.debug(f"Created folder for resource.")

    def download(self) -> None:
        """
        Additional download steps which
        download the direct request using requests.

        :return: None
        """
        r = requests.get(self.request.url, stream=True)
        total = r.headers.get("content-length")
        chunk_size = 1024
        dl = 0

        with open(f"{self.request.path}/{self.filename}{self.extension}", "wb+") as f:
            for chunk in r.iter_content(chunk_size):
                f.write(chunk)

                if total is not None:
                    progress = int((dl / int(total)) * 100)
                    if progress > self.request.progress:
                        self.request.set_progress(progress)
                    dl += chunk_size
