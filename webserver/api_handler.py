from asyncio import StreamReader, StreamWriter
import webserver.request_handler as request_handler
from webserver.SettingsController import SettingsControllerFactory
from webserver.RandomController import RandomControllerFactory2


class ApiHandler(request_handler.RequestHandler):
    controller_factories = []

    def __init__(self, request_lines: list[str], reader: StreamReader, writer: StreamWriter):
        super().__init__(request_lines, reader, writer)
        self.writer = writer
        self.controller_factories.append(SettingsControllerFactory())
        self.controller_factories.append(RandomControllerFactory2())

    async def handle_internal(self):
        await self.write_str('HTTP/1.0 200 OK\r\n')
        await self.write_str('Content-type: appilcation/json\r\n\r\n')
        # await self.write_str('{pin0 : 1}')
        response = str(self.handle_request())
        await self.write_str(response)

    def handle_request(self):
        url_path = self.get_url_path()
        for factory in self.controller_factories:
            controller = factory.try_create(url_path)  # type: ignore
            if controller is None:
                continue

            return controller.get()


if __name__ == '__main__':
    request_lines = ["GET api/settings"]
    handler = ApiHandler(request_lines, None, None)
    respose = handler.handle_request()
    print(respose)
