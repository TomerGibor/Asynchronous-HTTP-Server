""""
This module is used to parse HTTP requests sent by the HTTP client.
"""

from dataclasses import dataclass
from typing import Tuple

ROOT_DIR = "source_files/"


@dataclass
class RequestLineHeader:
    """ Model describing first request line."""
    method: str
    path: str
    http_version: str


def parse_request(request: bytes) -> Tuple[RequestLineHeader, str]:
    """
    Parse raw data request sent by client.

    Args:
        request: Data sent by client.

    Returns:
        Parsed request line header and additional arguments.
    """

    request = request.decode('ascii')
    print(request)
    split_request = request.split('\r\n')
    method, path, http_version = split_request[0].split(' ')
    path = ROOT_DIR + ('index.html' if path == '/' else path[1:])
    args = split_request[-1] if method == 'POST' else ''

    return RequestLineHeader(method, path, http_version), args


