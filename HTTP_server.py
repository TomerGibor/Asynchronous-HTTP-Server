"""
Asynchronous HTTP Server.
"""
import asyncio

from request_parser import parse_request
from request_handler import handle_request


class TcpServerProtocol(asyncio.Protocol):
    """
    Asynchronous TCP server.
    """

    def __init__(self):
        """
        :ivar Transport transport:  Transport that represents the connection with client.
        :ivar Tuple[str, int] peername: IPv4 Address of the client and port.
        """
        self.transport = None
        self.peername = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        Handle new connection with client.
        :param transport: The async object representing the connection with client.
        """
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        print(f'Connection from {self.peername}')

    def connection_lost(self, transport: asyncio.Transport) -> None:
        """
        Occurs when connection lost with client.

        :param transport: The async object representing the connection with client.
        """
        print(f'The client {self.peername} has closed the connection')

    def data_received(self, data: bytes) -> None:
        """
        Handle data received from client and send response.
        :param data: Raw data received from the client.
        """
        request_line_header, args = parse_request(data)
        handle_request(request_line_header, self.transport, args)
        # response = responder.handle_request(request_line_header, args)
        # self.transport.write(response)
