"""
Download utils.

This file contains functions and action not fit for standard Django files.
"""
import os

from src.download.models import BaseRequest


def list_files(request: BaseRequest) -> list:
    """
    List the file belonging to a BaseRequest.

    :param request: A BaseRequest object.
    :return: A list containing the files belonging to the BaseRequest.
    """
    content = []

    for root, dirs, files in os.walk(request.path):
        for dir in dirs:
            content.append({'path': f'{root}/{dir}', 'children': []})

        for file in files:
            sub_dirs = list(filter(lambda i: i['path'] == root, content))
            if len(sub_dirs):
                sub_dirs[0]['children'].append({'path': f'{root}/{file}', 'name': file})
            else:
                content.append({'path': f'{root}/{file}', 'name': file})

    return content
