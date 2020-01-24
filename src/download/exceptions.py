"""
Download exceptions.
"""


class BaseRequestModelException(Exception):
    """
    Exception related to the base request model.
    """
    pass


class BaseRequestSetStatusException(BaseRequestModelException):
    """
    Exception related to setting the status of the base request model.
    """
