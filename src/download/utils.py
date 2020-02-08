"""
Download utils.

This file contains functions and action not fit for standard Django files.
"""
import os


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
