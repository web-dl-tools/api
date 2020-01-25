"""
Download loggers
"""
import logging

from .models import BaseRequest, Log


class BaseLogger(logging.Logger):
    """
    Base logger.
    """
    request = None

    def __init__(self, request: BaseRequest, name, level=logging.NOTSET):
        """
        Initialize the logger.

        :param request: BaseRequest
        :param name: str
        :param level: int
        """
        self.request = request

        super().__init__(name, level)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        Intercept the Logger's LogRecord creation call and create a Download Log entity.

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
        if msg:
            Log.objects.create(request=self.request, level=level, message=msg.strip())
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
