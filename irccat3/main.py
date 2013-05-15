from __future__ import absolute_import

import argparse
import logging
import multiprocessing
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
                        type=int, default=6666)

    parser.add_argument("--listen-interface", help="increase output verbosity",
                        default='0.0.0.0')
    parser.add_argument("--listen-port", help="increase output verbosity",
                        type=int, default=12345)

    args = parser.parse_args(argv)

    return args

def main():

    logging.basicConfig(level=logging.DEBUG)
    log.error('TP')

    args = get_args(sys.argv[1:])

    q = Queue.Queue()
    #q = multiprocessing.Queue()
    
    log.info('pre l start')
    l = listener.Listener(q)
    l.start()
    log.info('past l start')

    b = bot.Bot(q)
    b.start()
    log.info('past b start')


    b.join()
    

# process options
# start bot in one thread
# start socket listener in another.
