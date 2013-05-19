import errno
import logging
import os
import select
import socket
import sys
import threading


log = logging.getLogger(__name__)


REQUEST_QUEUE_SIZE = 5


class TCPServer(threading.Thread):

    def __init__(self, q, host='localhost', port=9999):
        threading.Thread.__init__(self)

        self.q = q
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(REQUEST_QUEUE_SIZE)

    def process_request(self, request, client_address):
        rfile = request.makefile('rb', -1)

        try:
            while True:
                data = rfile.readline().strip()
                if not data:
                    break
                log.info("%r wrote: %r", client_address[0], data)

                self.q.put(data)
        finally:
            rfile.close()

        request.close()

    def _handle_request_noblock(self):
        """Handle one request, without blocking.

        I assume that select.select has returned that the socket is
        readable before this function was called, so there should be
        no risk of blocking in get_request().
        """
        try:
            request, client_address = self.socket.accept()
        except socket.error:
            return

        try:
            self.process_request(request, client_address)
        except Exception:
            log.error("Socket request error: %r %r", request, client_address)
            request.close()

    def run(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.serve_forever(0.1)

    def serve_forever(self, poll_interval=0.5):
        self.__is_shut_down.clear()
        try:
            while not self.__shutdown_request:
                # XXX: Consider using another file descriptor or
                # connecting to the socket to wake this up instead of
                # polling. Polling reduces our responsiveness to a
                # shutdown request and wastes cpu at all other times.
                self.wait_and_handle(poll_interval)
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def wait_and_handle(self, poll_interval):
        def _eintr_retry(func, *args):
            """restart a system call interrupted by EINTR"""
            while True:
                try:
                    return func(*args)
                except (OSError, select.error) as e:
                    if e.args[0] != errno.EINTR:
                        raise

        # XXX: Consider using another file descriptor or
        # connecting to the socket to wake this up instead of
        # polling. Polling reduces our responsiveness to a
        # shutdown request and wastes cpu at all other times.

        # r, w, e = _eintr_retry(select.select, [self.socket], [], [],
        #                        poll_interval)
        r, w, e = select.select([self.socket], [], [], poll_interval)
        if self.socket in r:
            self._handle_request_noblock()

    def shutdown(self):
        """Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__shutdown_request = True
        self.__is_shut_down.wait()
