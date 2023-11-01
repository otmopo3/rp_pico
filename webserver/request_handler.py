class RequestHandler():
    def __init__(self, request_lines, reader, writer):
        self.request_lines = request_lines
        self.reader = reader
        self.writer = writer

    async def handle(self):
        await self.handle_internal()

        await self.writer.drain()
        await self.writer.wait_closed()

    async def handle_internal(self):
        pass

    def get_url_path(self):
        return self.request_lines[0].split()[1]