"""
Youtube-dl handlers.
"""
import youtube_dl

from src.download.handlers import BaseHandler


class Handler(BaseHandler):
    """
    Youtube-dl handler.
    """
    options = None

    @staticmethod
    def handles(url: str) -> bool:
        """
        Notify if the given url can be handler by the handler.

        :param url: str
        :return: bool
        """
        return True

    def _pre_process(self) -> None:
        """
        Pre process the request.

        :return: None
        """
        self.options = {
            'format': self.request.format,
        }
        super()._pre_process()

    def _process(self) -> None:
        """
        Process the request.

        :return: None
        """
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.request.url])

        super().process()
