"""
Audio visual handlers.
"""
import youtube_dl

from src.download.handlers import BaseHandler


class Handler(BaseHandler):
    """
    Audio visual handler.
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
        super()._pre_process()
        self.options = {
            'outtmpl': f'{self.request.path}/%(title)s.%(ext)s',
            'format': self.request.format,
            'logger': self.logger,
            'progress_hooks': [self.progress_hook],
        }

    def _download(self) -> None:
        """
        Process the request.

        :return: None
        """
        super()._download()
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.request.url])

    def progress_hook(self, d: dict) -> None:
        """
        Progress hook for youtube-dl.

        :param d: dict
        :return: None
        """
        print(f'PROGRESS: {d}')
