"""
Audio visual handlers.

This file contains the BaseHandler implementation of the audio visual handler.
"""
import re
import youtube_dl

from .loggers import AudioVisualLogger
from src.download.models import BaseRequest
from src.download.handlers import BaseHandler, BaseHandlerStatus


class AudioVisualHandler(BaseHandler):
    """
    An audio visual handler which implements the BaseHandler object.
    """

    options = None

    def __init__(self, request: BaseRequest) -> None:
        """
        Initialize the handler object with an associated request.

        :param request: A BaseRequest containing the request options.
        :return: None
        """
        super().__init__(request)
        self.logger = AudioVisualLogger(
            self.request,
            f"logger.{self.request.get_handler_object().__name__}.{self.request.id}",
        )

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        from .models import AudioVisualRequest

        status = BaseHandlerStatus(AudioVisualRequest.__name__)
        status.set_description("A handler for downloading an audio and/or visual resource.")

        try:
            with youtube_dl.YoutubeDL({}) as ydl:
                meta = ydl.extract_info(url, download=False)
                formats = meta.get("formats", [meta])
                status.set_supported(True)
                status.set_options(formats)
        except Exception:
            status.set_supported(False)
            status.set_options({})

        return status

    def _pre_process(self) -> None:
        """
        An extension of the _pre_process method which configures the options
        for use when downloading the request.

        :return: None
        """
        super()._pre_process()

        with youtube_dl.YoutubeDL({}) as ydl:
            meta = ydl.extract_info(self.request.url, download=False)
            self.request.set_data(meta)
            self.request.set_title(meta["title"])

            self.options = {
                "verbose": True,
                "writedescription": True,
                "writeannotations": True,
                "write_all_thumbnails": True,
                "writesubtitles": True,
                "outtmpl": f"{self.request.path}/{self.request.output}",
                "format": self.request.format_selection,
                "logger": self.logger,
                "progress_hooks": [self.progress_hook],
            }

    def _download(self) -> None:
        """
        An extension of the _download method which
        download the audio visual request using youtube-dl.

        :return: None
        """
        super()._download()
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.request.url])

    def progress_hook(self, d: dict) -> None:
        """
        A progress hook function for youtube-dl which
        log's the progress to the request.

        :param d: dict
        :return: None
        """
        if "_percent_str" in d:
            matches = re.findall("\d+\.\d+", d["_percent_str"])
            progress = int(float(matches[0]))
            if progress > self.request.progress:
                self.request.set_progress(progress)
                if progress == 100:
                    self.request.set_status(BaseRequest.STATUS_POST_PROCESSING)
