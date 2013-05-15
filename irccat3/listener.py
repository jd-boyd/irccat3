import logging
import SocketServer
import threading
import multiprocessing

log = logging.getLogger(__name__)


class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, request, client_address, server, q=None):
        assert q
        self.q = q
        SocketServer.StreamRequestHandler.__init__(self, request, 
                                                   client_address, server)
        
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data = self.rfile.readline().strip()
        log.info("%r wrote: %r", self.client_address[0], data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.q.put(data)

class MyTcpServer(SocketServer.TCPServer):
    allow_reuse_address = True

#class Listener(multiprocessing.Process):
class Listener(threading.Thread):
    def __init__(self, q, host='localhost', port=9999):
        threading.Thread.__init__(self)
        #multiprocessing.Process.__init__(self)
        self.q = q
        self.host = host
        self.port = port

    def run(self):

        def handler_factory(*a, **kw):
            log.info("HF %r %r", a, kw)
            handler = MyTCPHandler(*a, q=self.q)

        # Create the server, binding to localhost on port 9999
        self.server = MyTcpServer((self.host, self.port), handler_factory)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.server.serve_forever(0.1)

    def stop(self):
        self.server.shutdown()
