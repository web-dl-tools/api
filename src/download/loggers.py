"""
Download loggers
"""
import logging

from .models import BaseRequest


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

    def debug(self, msg, *args, **kwargs):
        print(f'DEBUG: {msg}')
        super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        print(f'INFO: {msg}')
        super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        print(f'WARN: {msg}')
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        print(f'ERR: {msg}')
        super().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        print(f'CRIT: {msg}')
        super().critical(msg, *args, **kwargs)
