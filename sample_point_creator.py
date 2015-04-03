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
DEFAULT_ERRORS = 10

SYMBOLS = [
   # '^DJI',
   'AAPL',
   'AMZN',
   'AXP',
   'BA',
   'BAC',
   'BRCD',
   'C',
   'CAT',
   'CSCO',
   'CVX',
   'DATA',
   'DD',
   'DIJA',
   'DIS',
   'EBAY',
   'FB',
   'FEYE',
   'GE',
   'GOOG',
   'GRPN',
   'GS',
   'HD',
   'HPQ',
   'IBM',
   'INTC',
   'JNJ',
   'JPM',
   'KO',
   'LNKD',
   'MCD',
   'MMM',
   'MRK',
   'MSFT',
   'NFLX',
   'NKE',
   'PANW',
   'PFE',
   'PG',
   'SPLK',
   'SYMC',
   'TRV',
   'TSLA',
   'TWTR',
   'UNH',
   'UTX',
   'V',
   'VZ',
   'WDAY',
   'WFC',
   'WFM',
   'WMT',
   'XOM',
   'YHOO',
   'Z',
   'ZEN',
   '^IXIC',
   '^SPXPM',
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
    parser.add_argument('-e', '--error_max', default=DEFAULT_ERRORS, type=int,
            help='Maximum number of socket errors allowed before quitting.')
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
    errors = 0
    while count != 0 and errors < ARGS.error_max:
        if ARGS.send:
            sock = socket.socket()
            sock.connect((ARGS.host, ARGS.port))

        prices = ystockquote.get_tag(SYMBOLS, 'l1')
        if prices:
            for symbol in SYMBOLS:
                price = prices[symbol][0]
                symbol = symbol.replace('^', '')
                line = "stock.price %s host='%s'" % (price, symbol)

                print(line)
                if ARGS.send:
                    sock.sendall('%s\n' % line)

            if count > 0:
                count -= 1
            print('---- %d left to go ----' % count)
        else:
            errors += 1
            print('---- Retrying (%d errors) ----' % errors)

        if ARGS.send:
            sock.close()

        time.sleep(ARGS.delay)

    return errors


if __name__ == '__main__':
    ARGS = parse_args()
    sys.exit(main())
