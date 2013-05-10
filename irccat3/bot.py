import irc.client
import logging
import sys
import threading

log = logging.getLogger(__name__)


class IRCCat(irc.client.SimpleIRCClient):
    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target

    def on_welcome(self, connection, event):
        if irc.client.is_channel(self.target):
            connection.join(self.target)
        else:
            self.send_it()

    def on_join(self, connection, event):
        self.send_it()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def send_it(self):
        while 1:
            line = sys.stdin.readline().strip()
            if not line:
                break
            self.connection.privmsg(self.target, line)
        self.connection.quit("Using irc.client.py")

class Bot(threading.Thread):
    def __init__(self, q, host='localhost', port=9999):
        threading.Thread.__init__(self)
        self.q = q
        self.host = host
        self.port = port
    
    def run(self):
        pass
