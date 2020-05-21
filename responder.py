"""
Module to send HTTP response.
"""

import asyncio
from dataclasses import dataclass
from typing import List
from http import HTTPStatus

CONTENT_TYPES = {
    'HTML': 'text\html',
    'CSS': 'text\css',
    'PNG': 'image\png',
    'PHP': 'text\php'
}
IMAGE_FILES = ('PNG', 'JPEG', 'JPG')
INVALID_RESPONSE_HTML = '<html><body><h1> Invalid Client Request</h1></body></html>'


def send_file_response(path: str, http_version: str,
                       transport: asyncio.Transport) -> None:
    """
    Function used to send encoded file HTTP response on transport.

    Args:
        path: Path of the file requested by client.
        http_version: HTTP version.
        transport: The async object representing the connection with client.

    """

    file_type = path.split('.')[-1].upper()
    ok_response_line = ResponseLineHeader(http_version, HTTPStatus.OK, HTTPStatus.OK.phrase)
    response_headers = HTTPResponseHeaders(ok_response_line, list())
    try:
        with open(path, 'rb' if file_type in IMAGE_FILES else 'r') as f:
            body = f.read()
    except FileNotFoundError:
        print(f'Invalid client GET Request - File not found: {path.split("/")[-1]}')
        response_headers.response_line_header = ResponseLineHeader(
            http_version, HTTPStatus.NOT_FOUND, HTTPStatus.NOT_FOUND.phrase)
        body = INVALID_RESPONSE_HTML
        file_type = 'HTML'
    if file_type not in IMAGE_FILES:
        response_headers.headers.append(HTTPHeader('Charset', 'utf-8'))
    response_headers.headers.append(HTTPHeader('Content-Type',
                                               str(CONTENT_TYPES[file_type])))
    response_headers.headers.append(HTTPHeader('Content-Length', str(len(body))))
    response_headers.headers.append(HTTPHeader('Connection', 'Keep-Alive'))
    response = _get_response(file_type, response_headers, body)
    transport.write(response)


def _get_response(file_type: str, response_headers, body) -> bytes:
    """
    Function to create and return encoded HTTP response given
      response headers and body.

    Args:
        file_type: The type of file requested by client.
        response_headers: HTTP response headers.
        body: Body of the response.

    Returns:
        Encoded HTTP response.
    """

    return bytes(HTTPTextResponse(response_headers, body)) \
        if file_type not in IMAGE_FILES \
        else bytes(HTTPImageResponse(response_headers, body))


@dataclass
class HTTPHeader:
    """Model describing HTTP header."""

    header_type: str
    header_value: str

    def __str__(self):
        return f'{self.header_type}: {self.header_value}'


@dataclass
class ResponseLineHeader:
    """ Model describing first response line. """

    http_version: str
    status_code: int
    status_message: str

    def __str__(self):
        """ String representation of the model to be sent back to client."""
        return f"{self.http_version} {self.status_code} {self.status_message}"


@dataclass
class HTTPResponseHeaders:
    """ Model describing headers of a HTTP response."""

    response_line_header: ResponseLineHeader
    headers: List[HTTPHeader]

    def __str__(self):
        """Deserialization of the response headers."""
        deserialized_headers = str(self.response_line_header) + "\r\n"
        for http_header in self.headers:
            if http_header:
                deserialized_headers += str(http_header) + "\r\n"
        return deserialized_headers


@dataclass
class Body:
    """Body of the HTTP Request."""

    def body_content(self):
        pass


@dataclass
class TextBody(Body):
    """Body of a text HTTP response."""

    body_content: str

    def __str__(self):
        return self.body_content


@dataclass
class ImageBody(Body):
    """Body of an image HTTP response."""

    body_content: bytes

    def __bytes__(self):
        return self.body_content


@dataclass
class HTTPResponse:
    """HTTP response containing headers and body."""

    def response_headers(self):  # Of type HTTPResponseHeaders
        pass

    def body(self):  # Of type Body
        pass

    def __bytes__(self):
        pass


@dataclass
class HTTPTextResponse(HTTPResponse):
    """HTTP response with text body."""

    response_headers: HTTPResponseHeaders
    body: TextBody

    def __bytes__(self):
        """Deserialize and encode the text response to be sent to client."""
        return f'{str(self.response_headers)}\r\n{self.body}\r\n\r\n'.encode()


@dataclass
class HTTPImageResponse(HTTPResponse):
    """HTTP response with an image body."""

    response_headers: HTTPResponseHeaders
    body: ImageBody

    def __bytes__(self):
        """Deserialize and encode the image response to be sent to client."""
        return (str(self.response_headers) + '\r\n').encode() + bytes(self.body)
