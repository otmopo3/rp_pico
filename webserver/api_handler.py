import webserver.request_handler as request_handler


class ApiHandler(request_handler.RequestHandler):

    async def handle_internal(self):
        self.writer.write('HTTP/1.0 200 OK\r\n')
        self.writer.write('Content-type: appilcation/json\r\n\r\n')
        self.writer.write('{pin0 : 1}')
