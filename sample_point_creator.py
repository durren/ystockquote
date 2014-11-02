#!/usr/bin/env python
"""Sample test point creator.
"""
__copyright__ = 'Copyright (c) 2014 Wavefront Inc.'
__version__ = '0.1.0'

import socket
import sys
import time

import ystockquote


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 2878
TIME_INTERVAL = 10 #seconds
SYMBOLS = [
        'GOOG',
        '^SPXPM',
        'SPLK',
        'BAC',
        'FEYE',
        'WDAY',
        'NFLX',
        'DATA',
        'PANW',
        '^IXIC',
#        '^DJI',
        'AAPL',
        'WFC',
        'WFM',
        'JPM',
        'C',
        'ZEN',
        'TWTR',
        'FB',
        'MSFT',
        'Z',
        'SYMC',
        'TSLA',
        'GRPN',
        'EBAY',
        'BRCD',
        'XOM',
        'IBM',
        'AMZN',
        'HPQ',
        'LNKD',
        'YHOO',
        ]

get_more = True
while get_more:
#    sock = socket.socket()
#    sock.connect((DEFAULT_HOST, DEFAULT_PORT))
    prices = ystockquote.get_tag(SYMBOLS, 'l1')
    for symbol in SYMBOLS:
        price = prices[symbol][0]
        symbol = symbol.replace('^', '')
        line = 'stock.price %s host=%s' % (price, symbol)
        print(line)
#        sock.sendall('%s\n' % line)
#    sock.close()
    time.sleep(TIME_INTERVAL)
