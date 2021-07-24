"""
Download utils.

This file contains functions and action not fit for standard Django files.
"""
import os
import magic

from base64 import b64decode
from urllib.parse import unquote
from datetime import datetime

from wsgiref.util import FileWrapper
from django.http import FileResponse

from src.user.models import User
from .models import BaseRequest


def calculate_storage(path: str) -> int:
    """
    Calculate the storage for a folder.

    :param path: The path to calculate
    :return: The storage in bytes.
    """
    size = 0

    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            size += calculate_storage(f"{root}/{_dir}")

        for file in files:
            size += os.path.getsize(f"{root}/{file}")
        break

    return size


def list_files(path: str) -> list:
    """
    List all files of the given directory and recursively
    traverses down all folders to do the same.

    :param path: A str of the path to list the files of.
    :return: A list containing the files belonging to root path.
    """
    content = []

    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            content.append(
                {
                    "dir": f"{root}/{_dir}",
                    "name": _dir,
                    "children": list_files(f"{root}/{_dir}"),
                }
            )

        for file in files:
            filename, extension = os.path.splitext(file)
            content.append(
                {
                    "path": f"{root}/{file}",
                    "name": file,
                    "filename": filename,
                    "extension": extension,
                    "size": os.path.getsize(f"{root}/{file}"),
                    "created_at": datetime.fromtimestamp(os.path.getmtime(f"{root}/{file}")),
                }
            )
        break

    return content


def prepare_path(path: str) -> str:
    """
    Decode and normalize the path for usage when retrieving a file from the files folder.
    This step must be performed on all user provided paths in order to prevent uncontrolled data used in path expression.

    :param path: The raw user provided path value.
    :return: A decoded and normalized path.
    """
    path = unquote(b64decode(path).decode('utf-8'))
    path = os.path.normpath(path)

    return path


def validate_user_path(path_parts: list, user: User) -> bool:
    """
    Validate a request file path to ensure only the authorized user
    for the user folder may have file retrieval access.

    :param path_parts: A list of path parts of the relative file path.
    :param user: The currently authenticated user.
    :return: A bool containing the access result.
    """
    if len(path_parts) < 2:
        return False

    if path_parts[0] != "files":
        return False

    if path_parts[1] != str(user.id):
        return False

    return True

def validate_for_request(path: str, user: User) -> bool:
    """
    Validate a request folder file path to ensure only the authorized user
    for the request may have file retrieval access.

    :param path: A str containing the relative file path.
    :param user: The currently authenticated user.
    :return: A bool containing the access result.
    """
    path_parts = path.split("/")

    if not validate_user_path(path_parts, user):
        return False

    if len(path_parts) < 4:
        return False

    if not BaseRequest.objects.filter(id=path_parts[2], user=user).exists():
        return False

    return True

def validate_for_archive(path: str, user: User) -> bool:
    """
    Validate a request archive file path to ensure only the authorized user
    for the request may have archive retrieval access.

    :param path: A str containing the relative archive path.
    :param user: The currently authenticated user.
    :return: A bool containing the access result.
    """
    path_parts = path.split("/")

    if not validate_user_path(path_parts, user):
        return False

    if len(path_parts) != 3:
        return False

    if not BaseRequest.objects.filter(id=path_parts[2].replace('.zip', ''), user=user).exists():
        return False

    if not os.path.isfile(path):
        return False

    return True


def create_file_streaming_response(path: str) -> FileResponse:
    """
    Create a streaming file response to serve the file while
    reducing the memory usage in order to support large file
    downloads, particularly on memory limited hardware.
    The file will always be force downloaded as attachment if
    the file size exceeds a given limit, else it is up to the
    client to decide how to process and view the file.

    :param path: A str containing the file path.
    :return: A FileResponse containing a streaming file.
    """
    filename = os.path.basename(path)
    filename = filename.replace(',', '').replace(';', '-')
    file_size = os.path.getsize(path)
    mime = magic.Magic(mime=True)
    attachment = file_size > 5000000  # 5 MB
    chunk_size = 32000    # 32 KB

    response = FileResponse(
        FileWrapper(open(path, "rb", buffering=chunk_size), blksize=chunk_size),
        as_attachment=attachment
    )

    response["Content-Length"] = os.path.getsize(path)
    response["Content-Type"] = mime.from_file(path)
    response[
        "Content-Disposition"
    ] = f"{'attachment' if attachment else 'inline'}; filename=\"{filename}\""

    return response
