"""
Audio visual handlers.

This file contains the BaseHandler implementation of the audio visual handler.
"""
import youtube_dl

from src.download.handlers import BaseHandler, BaseHandlerStatus


class AudioVisualHandler(BaseHandler):
    """
    a Audio visual handler which implements the BaseHandler object.
    """
    options = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        from .models import AudioVisualRequest

        status = BaseHandlerStatus(AudioVisualRequest.__name__)
        status.set_supported(True)   # TODO: traverse youtube-dl extractors for support status.

        try:
            with youtube_dl.YoutubeDL({}) as ydl:
                meta = ydl.extract_info(url, download=False)
                formats = meta.get('formats', [meta])
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
        self.options = {
            # 'verbose': True,
            # 'writedescription': True,
            # 'writeannotations': True,
            # 'writethumbnail': True,
            # 'writesubtitles': True,
            'outtmpl': f'{self.request.path}/%(title)s.%(ext)s',
            'format': self.request.format_selection,
            'logger': self.logger,
            'progress_hooks': [self.progress_hook],
        }
        print(self.options)

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
        a Progress hook function for youtube-dl which log's the progress to stdout.

        :param d: dict
        :return: None
        """
        print(f'PROGRESS: {d}')
