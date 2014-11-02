#!/usr/bin/env python
"""Sample test point creator.
"""
__copyright__ = 'Copyright (c) 2014 Wavefront Inc.'
__version__ = '0.1.0'

import socket
import sys
import time

from argparse import ArgumentParser

import ystockquote


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 2878
DEFAULT_DELAY = 10 #seconds
DEFAULT_COUNT = -1

SYMBOLS = [
        'AAPL',
        'AMZN',
        'BAC',
        'BRCD',
        'C',
        'DATA',
#        '^DJI',
        'EBAY',
        'FB',
        'FEYE',
        'GOOG',
        'GRPN',
        'HPQ',
        'IBM',
        '^IXIC',
        'JPM',
        'LNKD',
        'MSFT',
        'NFLX',
        'PANW',
        'SPLK',
        '^SPXPM',
        'SYMC',
        'TSLA',
        'TWTR',
        'WDAY',
        'WFC',
        'WFM',
        'XOM',
        'YHOO',
        'Z',
        'ZEN',
        ]


def parse_args():
    """Parse user arguments and return as parser object.

    Returns:
        Parser object with arguments as attributes.
    """
    parser = ArgumentParser(description='Create ystockquote test points.')
    parser.add_argument('-s', '--host', default=DEFAULT_HOST,
            help='Host IP of machine running agent.')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int,
            help='Port on host.')
    parser.add_argument('-d', '--delay', default=DEFAULT_DELAY, type=int,
            help='Delay between queries, in seconds.')
    parser.add_argument('-c', '--count', default=DEFAULT_COUNT,
            type=int, help='Number of iterations; negative for infinite.')
    parser.add_argument('-S', '--send', action='store_true',
            help='Send points to host for real.')
    args = parser.parse_args()
    return args


def main():
    """Main script.
    """
    count = ARGS.count
    while count != 0:
        if ARGS.send:
            sock = socket.socket()
            sock.connect((ARGS.host, ARGS.port))

        prices = ystockquote.get_tag(SYMBOLS, 'l1')
        for symbol in SYMBOLS:
            price = prices[symbol][0]
            symbol = symbol.replace('^', '')
            line = 'stock.price %s host=%s' % (price, symbol)

            if ARGS.send:
                sock.sendall('%s\n' % line)
            else:
                print(line)

        if count > 0:
            count -= 1

        if ARGS.send:
            sock.close()
        else:
            print('---- %d left to go (of %d) ----' % (count, ARGS.count))

        time.sleep(ARGS.delay)


if __name__ == '__main__':
    ARGS = parse_args()
    main()
