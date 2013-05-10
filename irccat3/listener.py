import logging
import SocketServer
import threading

log = logging.getLogger(__name__)


class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

class Listener(threading.Thread):
    def __init__(self, q, host='localhost', port=9999):
        threading.Thread.__init__(self)
        self.q = q
        self.host = host
        self.port = port
    
    def run(self):

        # Create the server, binding to localhost on port 9999
        server = SocketServer.TCPServer((self.host, self.port), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
