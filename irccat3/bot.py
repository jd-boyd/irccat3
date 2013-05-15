import irc.client
import logging
import sys
import threading
import time

log = logging.getLogger(__name__)


class IRCCat(irc.client.SimpleIRCClient):
    def __init__(self, target, q):
        log.info('IC init')
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target
        self.q = q

    def on_welcome(self, connection, event):
        log.info('OW')
        if irc.client.is_channel(self.target):
            connection.join(self.target)
        else:
            self.send_it()

    def on_join(self, connection, event):
        log.info('OJ')
        self.send_it()

    def on_disconnect(self, connection, event):
        log.info('OD')
        sys.exit(0)

    def send_it(self):
        log.info('SI')
        while 1:
            log.info('SPIN')
            line = self.q.get(True)
            self.connection.privmsg(self.target, line)
        self.connection.quit("Using irc.client.py")

class Bot(threading.Thread):
    def __init__(self, q, host='10.0.3.178', port=6667):
        threading.Thread.__init__(self)
        self.q = q
        self.host = host
        self.port = port
    
    def run(self):
        log.info("BR:")
        c = IRCCat("#chat", self.q)
        c.connect(self.host, self.port, "catbot")
        c.start()

    def stop(self):
        #self.
        pass