from __future__ import absolute_import

import argparse
import logging
import multiprocessing
import Queue
import signal
import sys
import threading

from irccat3 import bot, listener

log = logging.getLogger(__name__)


def get_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--verbosity", help="increase output verbosity")

    parser.add_argument("--irc-server", help="IRC server to connect to.",
                        default='localhost')
    parser.add_argument("--irc-port", help="Port for irc server",
                        type=int, default=6667)
    parser.add_argument("--irc-channel", help="IRC channel to publish to",
                        default='#irccat')

    parser.add_argument("--listen-interface", 
                        help="network interface to listen on.  Defaults to all of them.",
                        default='0.0.0.0')
    parser.add_argument("--listen-port", 
                        help="Port to listen on (default 12345)",
                        type=int, default=12345)

    args = parser.parse_args(argv)

    return args

l = None

def signal_handler(signal, frame):
    log.info('SIG %r', signal)
    l.stop()
    sys.exit(0)

def main():

    logging.basicConfig(level=logging.INFO)

    args = get_args(sys.argv[1:])

    log.info('args: %r', args)

    signal.signal(signal.SIGINT, signal_handler)

    q = Queue.Queue()
    
    l = listener.Listener(q, host=args.listen_interface, 
                          port=args.listen_port)
    l.start()

    b = bot.Bot(q, host=args.irc_server, port=args.irc_port, 
                channel=args.irc_channel)
    b.start()

    b.join()
    l.stop()

