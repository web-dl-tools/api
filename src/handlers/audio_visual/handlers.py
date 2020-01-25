"""
Audio visual handlers.
"""
import youtube_dl

from src.download.handlers import BaseHandler, BaseHandlerStatus


class AudioVisualHandler(BaseHandler):
    """
    Audio visual handler.
    """
    options = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify if the given url can be handler by the handler.

        :param url: str
        :return: bool
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
        Pre process the request.

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
