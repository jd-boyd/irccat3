from __future__ import absolute_import

from Queue import Queue
import socket
import time

from nose.tools import eq_

from irccat3 import listener

def send_stuff(host, port, stuff):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(stuff)
    client.close()

def test_listener():
    q = Queue()
    l = listener.Listener(q)
    print "R:"
    l.start()
    time.sleep(0.1)
    send_stuff('localhost', 9999, "#chat hello")
    print "S:"
    l.stop()

    eq_(q.get(), "#chat hello")
    

if __name__=="__main__":
    test_listener()
