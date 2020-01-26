"""
Download exceptions.

This file contains custom exceptions for the download actions
for more precise handling when errors occur.
"""


class BaseRequestModelException(Exception):
    """
    a base exception related to the base request model.
    This must only be used as a parent exception.
    """
    pass


class BaseRequestSetStatusException(BaseRequestModelException):
    """
    an exception related to incorrectly setting the status of the base request model.
    """
