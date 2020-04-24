""""
This module is used to parse HTTP requests sent by the HTTP client.
"""

from dataclasses import dataclass

ROOT_DIR = "source_files/"


@dataclass
class RequestLineHeader:
    """ Model describing first request line. """
    method: str
    path: str
    http_version: str


def parse_request(request: bytes) -> RequestLineHeader:
    """
    Parse raw data request sent by client.

    :param request: Data sent by client.
    :return: Parsed request line header and additional arguments.
    """
    request = request.decode("ascii")
    split_request = request.split("\r\n")
    method, path, http_version = split_request[0].split(" ")
    if path == "favicon.ico":
        path = "favicon.png"
    path = ROOT_DIR + ("index.html" if path == "/" else path[1:])
    args = split_request[-1] if method == "POST" else ""

    return RequestLineHeader(method, path, http_version), args


