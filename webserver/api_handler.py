import webserver.request_handler as request_handler


class ApiHandler(request_handler.RequestHandler):
    def __init__(self, request_lines, reader, writer):
        self.controllers = []
        super().__init__(request_lines, reader, writer)
    
    async def handle_internal(self):
        self.writer.write('HTTP/1.0 200 OK\r\n')
        self.writer.write('Content-type: appilcation/json\r\n\r\n')
        self.writer.write('{pin0 : 1}')

    def handle_request(self, request_line, writer):

        handeled = self.try_handle_api(request_line, writer)
        if (handeled):
            return


    def try_handle_api(self, path, writer):
        controller = self.try_find_controller(path)
        return "dasd"

    def try_find_controller(self, path):
        for controller in self.controllers:
            if controller.path == path:
                return controller

        return False