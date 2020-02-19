"""
Download utils.

This file contains functions and action not fit for standard Django files.
"""
import os
from wsgiref.util import FileWrapper
from django.http import FileResponse

from src.user.models import User
from .models import BaseRequest


def list_files(path: str) -> list:
    """
    List all files of the given directory and recursively traverses down all folders to do the same.

    :param path: A str of the path to list the files of.
    :return: A list containing the files belonging to root path.
    """
    content = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            content.append(
                {
                    "dir": f"{root}/{dir}",
                    "name": dir,
                    "children": list_files(f"{root}/{dir}"),
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
                }
            )
        break

    return content


def validate_path(path: str, user: User) -> bool:
    """
    Validate a request file path to ensure only the authorized user for
    the request may retrieve file access.

    :param path: A str containing the relative file path.
    :param user: The currently authenticated user.
    :return: A bool containing the access result.
    """
    path_parts = path.split("/")

    if len(path_parts) < 4:
        return False

    if path_parts[0] != "files":
        return False

    if int(path_parts[1]) != user.id:
        return False

    if not BaseRequest.objects.filter(id=path_parts[2], user=user).exists():
        return False

    return True


def create_file_streaming_response(path: str) -> FileResponse:
    """
    Create a streaming file response to serve the file while
    reducing the memory usage in order to support large file
    downloads, especially on memory limited hardware.

    :param path: A str containing the file path.
    :return: A FileResponse containing a streaming file.
    """
    filename = os.path.basename(path)
    chunk_size = 65536  # 64 kilobytes
    response = FileResponse(
        FileWrapper(open(path, "rb"), chunk_size), as_attachment=True
    )
    response["Content-Length"] = os.path.getsize(path)
    response["Content-Disposition"] = "attachment; filename=%s" % filename
    return response
