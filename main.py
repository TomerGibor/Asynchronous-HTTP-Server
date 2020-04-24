"""
Asynchronous HTTP Server
"""
import asyncio

from HTTP_server import TcpServerProtocol

IP = "0.0.0.0"
PORT = 8080


async def main() -> None:
    loop = asyncio.get_event_loop()
    server = await loop.create_server(lambda: TcpServerProtocol(), IP, PORT)

    async with server:
        print(f"Server listening on {IP}:{PORT}")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
