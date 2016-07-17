from __future__ import absolute_import, print_function

try:
    from Queue import Queue #py2
except:
    from queue import Queue #py3

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
    l = listener.TCPServer(q)
    print("R:")
    time.sleep(0.1)
    send_stuff('localhost', 9999, b"#chat hello")
    print("S:")

    l.wait_and_handle(0.5)

    eq_(q.get(), b"#chat hello")
