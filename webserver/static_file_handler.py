import asyncio
import webserver.request_handler as request_handler


class StaticFileHandler(request_handler.RequestHandler):
    async def handle_internal(self):
        url_path = self.get_url_path()
        file_path = url_path[1:].decode('utf-8')
        print(f"StaticFileHandler: Serving static file: {file_path}")

        try:
            file = open(f"/web/{file_path}", "r")
        except Exception as ex:
            print(f"StaticFileHandler: Error serving file {file_path}:")
            print(ex)
            await self.write_str('HTTP/1.0 404 Not found\r\n\r\n')
            return

        content = file.read()

        await self.write_ok(content, "text/html")


async def main():
    req_lines = [b"GET /index.html HTTP/1.1\r\n"]
    handler = StaticFileHandler(req_lines, None, None)

    await handler.handle_internal()

    req_lines = [b"GET /fdsf.html HTTP/1.1\r\n"]
    handler = StaticFileHandler(req_lines, None, None)

    await handler.handle_internal()


if __name__ == '__main__':
    asyncio.run(main())
