class ResponseTypes:
    TEXT: str = "text"
    OBJECT: str = "object"


class Controller:
    path: str
    response_type: ResponseTypes

    async def get(self):
        pass

    async def post(self, body: str):
        pass


class ControllerFactory:
    controller_path: str

    def try_create(self, request_line: str) -> Controller:
        print(
            f"type={__class__}, self.controller_path={self.controller_path}, request_line={request_line}")
        if self.controller_path in request_line:
            return self.create_controller()

        return None  # type: ignore

    def create_controller(self) -> Controller:
        return Controller()
