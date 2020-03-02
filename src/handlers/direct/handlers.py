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
        status.set_description("A handler for directly downloading the url resource.")
        status.set_options({})

        try:
            r = requests.head(url, allow_redirects=True)
            status.set_supported(r.status_code == 200)
        except requests.exceptions.InvalidSchema:
            status.set_supported(False)

        return status

    def _pre_process(self) -> None:
        super()._pre_process()

        r = requests.head(self.request.url, allow_redirects=True)
        headers = r.headers
        self.request.set_data(dict(headers))

        content_type = headers["content-type"].split(";")[0]
        self.extension = mimetypes.guess_extension(content_type)
        self.filename = (
            re.findall("filename=(.+)", headers["Content-Disposition"])[0]
            if "Content-Disposition" in headers.keys()
            else self.request.url.split("/")[-1]
        )
        if self.filename.endswith(self.extension):
            self.filename = self.filename[:-len(self.extension)]
        self.request.set_title(self.filename)

        if not os.path.exists(self.request.path):
            os.makedirs(self.request.path)

    def _download(self) -> None:
        """
        An extension of the _download method which
        download the direct request using requests.

        :return: None
        """
        super()._download()

        r = requests.get(self.request.url, stream=True)
        total = r.headers.get("content-length")
        dl = 0

        with open(f"{self.request.path}/{self.filename}{self.extension}", "wb+") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

                if total is not None:
                    progress = int((dl / int(total)) * 100)
                    if progress > self.request.progress:
                        self.request.set_progress(progress)
                    dl += 1024
