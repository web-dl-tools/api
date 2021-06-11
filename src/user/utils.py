"""
User utils.

This file contains functions and action not fit for standard Django files.
"""
import os


def get_storage_bytes(path: str) -> int:
    """
    Get the storage bytes total for the user directory.

    :param path: The user directory
    :return: The storage bytes
    """
    storage_bytes = 0

    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            storage_bytes += get_storage_bytes(f"{root}/{_dir}")

        for file in files:
            storage_bytes += os.path.getsize(f"{root}/{file}")
        break

    return storage_bytes
