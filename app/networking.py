from socketserver import TCPServer, BaseRequestHandler


class RequestHandler(BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        if self.data.startswith('query ordine'):
            id = self.data.split('"')[1]
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


server = TCPServer(('localhost', 5000), RequestHandler)
