from asyncio import StreamReader, StreamWriter


class RequestHandler():
    def __init__(self, request_lines: list[str], reader: StreamReader, writer: StreamWriter):
        self.request_lines = request_lines
        self.reader = reader
        self.writer = writer

    async def handle(self) -> None:
        await self.handle_internal()

        await self.writer.drain()
        await self.writer.wait_closed()

    async def write_ok(self, content: str, content_type: str) -> None:
        await self.write_str('HTTP/1.0 200 OK\r\n')
        await self.write_str(f'Content-type: {content_type}\r\n\r\n')
        await self.write_str(content)

    async def write_str(self, str: str) -> None:
        self.writer.write(str.encode())

    async def handle_internal(self):
        pass

    def get_url_path(self) -> str:
        return self.request_lines[0].split()[1]
