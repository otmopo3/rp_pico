from asyncio import StreamReader, StreamWriter
from webserver.ImputPinController import InputPinControlerFactory
import webserver.request_handler as request_handler
from webserver.SettingsController import SettingsControllerFactory
from webserver.RandomController import RandomControllerFactory2
from utils.json_serializer import JsonSerializer


class ApiHandler(request_handler.RequestHandler):
    controller_factories = []

    def __init__(self, request_lines: list[str], reader: StreamReader, writer: StreamWriter):
        super().__init__(request_lines, reader, writer)
        self.writer = writer
        self.controller_factories.append(SettingsControllerFactory())
        self.controller_factories.append(RandomControllerFactory2())
        self.controller_factories.append(InputPinControlerFactory())

    async def handle_internal(self):
        await self.write_str('HTTP/1.0 200 OK\r\n')
        await self.write_str('Content-type: appilcation/json\r\n\r\n')
        response = self.handle_request()

        await self.write_str(response)

    def handle_request(self) -> str:
        url_path = self.get_url_path()
        for factory in self.controller_factories:
            controller = factory.try_create(url_path)  # type: ignore
            if controller is None:
                continue

            response = controller.get()
            if (type(response) != str):
                print("serializing response")
                json_helper = JsonSerializer(response)
                response = json_helper.Serialize()

            return response

        return None  # type: ignore


if __name__ == '__main__':
    request_lines = ["GET api/input_pin_value"]
    handler = ApiHandler(request_lines, None, None)  # type: ignore
    respose = handler.handle_request()
    print(respose)
