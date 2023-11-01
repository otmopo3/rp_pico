import asyncio

from webserver.api_handler import ApiHandler
from webserver.static_file_handler import StaticFileHandler
try:
    import usocket as socket
except:
    import socket


class Webserver():
    def __init__(self, controllers, port=8080, api_prefix="api", web_folder="web"):
        self.controllers = controllers
        self.port = port

    async def run(self, tsf):
        asyncio.create_task(asyncio.start_server(
            self.serve_client, "0.0.0.0", self.port))
        while not tsf.is_set():
            print("server is working")
            await asyncio.sleep(60)

    async def serve_client(self, reader, writer):
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

    def handle_request(self, request_line, writer):

        handeled = self.try_handle_api(request_line, writer)
        if (handeled):
            return

        if (not handeled):
            self.handle_static_file(request_line, writer)
            return

    def handle_static_file(self, path, writer):
        return "dasd"

    def try_handle_api(self, path, writer):
        controller = self.try_find_controller(path)
        return "dasd"

    def try_find_controller(self, path):
        for controller in self.controllers:
            if controller.path == path:
                return controller

        return False


class Controller():
    def __init__(self, path):
        self.path = path

    def get(self, request_line):
        raise NotImplementedError()

    def post(self):
        raise NotImplementedError()


class HelloController(Controller):
    def __init__(self):
        self.path = "hello"

    def get(self, request_line):
        return "hello, web"


async def main():

    controllers = []
    webserver = Webserver(controllers)

    tsf = asyncio.Event()  # type: ignore

    task = asyncio.create_task(webserver.run(tsf))

    while True:
        await asyncio.sleep(10)

if __name__ == '__main__':
    import settings_module
    import wifi_network_module
    settings = settings_module.load_settings()
    wifi_network_module.connect_wifi(
        settings.wifi_ssid, settings.wifi_password)
    asyncio.run(main())
