"""
Application utils.

This file contains functions and action not fit for standard Django files.
"""
import subprocess
import json

from django.conf import settings


def get_build_info() -> dict:
    """
    Retrieve the latest git log and parse it to a python dictionary object.
    """
    log = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:\'{%n  "commit": "%H",%n  "abbreviated_commit": "%h",%n  "tree": "%T",%n  "abbreviated_tree": "%t",%n  "parent": "%P",%n  "abbreviated_parent": "%p",%n  "refs": "%D",%n  "encoding": "%e",%n  "subject": "%s",%n  "sanitized_subject_line": "%f",%n  "body": "%b",%n  "commit_notes": "%N",%n  "verification_flag": "%G?",%n  "signer": "%GS",%n  "signer_key": "%GK",%n  "author": {%n    "name": "%aN",%n    "date": "%aD"%n  },%n  "commiter": {%n    "name": "%cN",%n    "date": "%cD"%n  }%n},\'\n']).decode("utf-8")[1:-3]
    build = json.loads(log)
    build['version'] = settings.VERSION

    return build
