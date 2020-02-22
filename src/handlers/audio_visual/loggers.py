"""
Audio visual loggers.

This file contains a custom BaseLogger object for use by the AudioVisualHandler.
"""
from src.download.loggers import BaseLogger


class AudioVisualLogger(BaseLogger):
    """
    A audio visual logger object which intercepts Logger calls.
    """

    def makeRecord(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ):
        """
        Intercept the Logger's LogRecord creation call and create a Download Log entity.
        This add's an additional check to prevent download progress logs from being logged.

        :param name: *
        :param level: int
        :param fn: *
        :param lno: *
        :param msg: str
        :param args: *
        :param exc_info: *
        :param func: *
        :param extra: *
        :param sinfo: *
        :return: *
        """
        if all(s in msg for s in ("[download]", "% of ", "at", "ETA")):
            msg = ''

        return super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )
