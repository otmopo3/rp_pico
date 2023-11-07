import asyncio

from webserver.api_handler import ApiHandler
from webserver.static_file_handler import StaticFileHandler
try:
    import usocket as socket
except:
    import socket


class Webserver():
    def __init__(self, port=8080, api_prefix="api", web_folder="web"):

        self.port = port

    async def run(self, tsf):
        asyncio.create_task(asyncio.start_server(
            self.serve_client, "0.0.0.0", self.port))
        while not tsf.is_set():
            print("server is working")
            await asyncio.sleep(60)

    async def serve_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        print("Client connected")

        request_lines = []
        cur_line = await reader.readline()
        while cur_line != b"\r\n":
            request_lines.append(cur_line)
            print(cur_line)
            cur_line = await reader.readline()

        req_line = request_lines[0]
        if ("/api/" in req_line):
            request_handler = ApiHandler(request_lines, reader, writer)
        else:
            request_handler = StaticFileHandler(request_lines, reader, writer)

        await request_handler.handle()

        print("Client disconnected")


async def main():
    webserver = Webserver()
    tsf = asyncio.Event()  # type: ignore
    task = asyncio.create_task(webserver.run(tsf))

    while True:
        await asyncio.sleep(10)

if __name__ == '__main__':
    import utils.settings_module as settings_module
    import utils.wifi_network_module as wifi_network_module
    settings = settings_module.load_settings()
    wifi_network_module.connect_wifi(
        settings.wifi_ssid, settings.wifi_password)
    asyncio.run(main())
