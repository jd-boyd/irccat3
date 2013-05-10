from __future__ import absolute_import

import argparse
import logging
import Queue
import sys
import threading

from irccat3 import bot, listener

log = logging.getLogger(__name__)


def get_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--verbosity", help="increase output verbosity")

    parser.add_argument("--irc-server", help="increase output verbosity")
    parser.add_argument("--irc-port", help="increase output verbosity",
                        default='6666')

    parser.add_argument("--listen-interface", help="increase output verbosity",
                        default='0.0.0.0')
    parser.add_argument("--listen-port", help="increase output verbosity",
                        default='12345')

    parser.parse_args(argv)

    return {}

def main():

    logging.basicConfig()

    args = get_args(sys.argv[1:])

    q = Queue.Queue()
    
    l = listener.Listener(q)
    l.start()

    b = bot.Bot(q)
    b.start()

    b.join()
    

# process options
# start bot in one thread
# start socket listener in another.
