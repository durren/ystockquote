"""ystockquote : Retrieve stock quote data from Yahoo Finance

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

license: GNU LGPL

Requires: Python 2.7/3.3+
"""
__author__ = 'Corey Goldberg (cgoldberg@gmail.com)'
__copyright__ = 'Copyright (c) 2007, 2008, 2013 Corey Goldberg'
__version__ = '0.3.0'

import csv

try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode


QUOTE_URL = 'http://finance.yahoo.com/d/quotes.csv'
TABLE_URL = 'http://ichart.yahoo.com/table.csv'
SPECIAL_TAGS = {
    'dividend_yield': 'y',
    'dividend_per_share': 'd',
    'ask_realtime': 'b2',
    'dividend_pay_date': 'r1',
    'bid_realtime': 'b3',
    'ex_dividend_date': 'q',
    'previous_close': 'p',
    'today_open': 'o',
    'change': 'c1',
    'last_trade_date': 'd1',
    'change_percent_change': 'c',
    'trade_date': 'd2',
    'change_realtime': 'c6',
    'last_trade_time': 't1',
    'change_percent_realtime': 'k2',
    'change_percent': 'p2',
    'after_hours_change': 'c8',
    'change_200_sma': 'm5',
    'commission': 'c3',
    'percent_change_200_sma': 'm6',
    'todays_low': 'g',
    'change_50_sma': 'm7',
    'todays_high': 'h',
    'percent_change_50_sma': 'm8',
    'last_trade_realtime_time': 'k1',
    '50_sma': 'm3',
    'last_trade_time_plus': 'l',
    '200_sma': 'm4',
    'last_trade_price': 'l1',
    '1_year_target': 't8',
    'todays_value_change': 'w1',
    'holdings_gain_percent': 'g1',
    'todays_value_change_realtime': 'w4',
    'annualized_gain': 'g3',
    'price_paid': 'p1',
    'holdings_gain': 'g4',
    'todays_range': 'm',
    'holdings_gain_percent_realtime': 'g5',
    'todays_range_realtime': 'm2',
    'holdings_gain_realtime': 'g6',
    '52_week_high': 'k',
    'more_info': 'v',
    '52_week_low': 'j',
    'market_cap': 'j1',
    'change_from_52_week_low': 'j5',
    'market_cap_realtime': 'j3',
    'change_from_52_week_high': 'k4',
    'float_shares': 'f6',
    'percent_change_from_52_week_low': 'j6',
    'company_name': 'n',
    'percent_change_from_52_week_high': 'k5',
    'notes': 'n4',
    '52_week_range': 'w',
    'shares_owned': 's1',
    'stock_exchange': 'x',
    'shares_outstanding': 'j2',
    'volume': 'v',
    'ask_size': 'a5',
    'bid_size': 'b6',
    'last_trade_size': 'k3',
    'ticker_trend': 't7',
    'average_daily_volume': 'a2',
    'trade_links': 't6',
    'order_book_realtime': 'i5',
    'high_limit': 'l2',
    'eps': 'e',
    'low_limit': 'l3',
    'eps_estimate_current_year': 'e7',
    'holdings_value': 'v1',
    'eps_estimate_next_year': 'e8',
    'holdings_value_realtime': 'v7',
    'eps_estimate_next_quarter': 'e9',
    'revenue': 's6',
    'book_value': 'b4',
    'ebitda': 'j4',
    'price_sales': 'p5',
    'price_book': 'p6',
    'pe': 'r',
    'pe_realtime': 'r2',
    'peg': 'r5',
    'price_eps_estimate_current_year': 'r6',
    'price_eps_estimate_next_year': 'r7',
    'short_ratio': 's7',
    }


def _request(symbols, tag):
    """
    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.
        tag: Special tag or, confusingly, special tag combination.
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    symbol_string = '+'.join(symbols)
    url = '%s?s=%s&f=%s' % (QUOTE_URL, symbol_string, tag)
    req = Request(url)
    resp = urlopen(req)
    csv_content = resp.read().decode().strip()
    csv_reader = csv.reader(csv_content.split('\n'), delimiter=',')
    content = [row for row in csv_reader]
    return_dict = {}
    for index, symbol in enumerate(symbols):
        return_dict[symbol] = content[index]
    return return_dict


def get_all(symbols):
    """
    Get all available quote data for the given ticker symbols.

    Returns a dictionary.
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    tag_names_ordered = SPECIAL_TAGS.keys()
    tags = [SPECIAL_TAGS[tag_name] for tag_name in tag_names_ordered]
    tag_string = ''.join(tags)
    symbol_data = _request(symbols, tag_string)
    symbol_dict = {}
    for symbol in symbols:
        symbol_dict[symbol] = {}
        for index, tag_name in enumerate(tag_names_ordered):
            symbol_dict[symbol][tag_name] = symbol_data[symbol][index]
    return symbol_dict


def get_tag(symbols, tag):
    """
    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.
        tag: Special tag name, special tag, or, confusingly, special tag
        combination.  Examples:
            'trade_date' # special tag name
            'd2'         # special tag
            'nd1d2'      # special tag combination

    Returns:
        Dictionary of symbols with list of tag values requested.
    """
    if tag in SPECIAL_TAGS:
        tag = SPECIAL_TAGS[tag]
    return _request(symbols, tag)


def get_historical_prices(symbol, start_date, end_date):
    """Get historical prices for the given ticker symbol.

    TODO: The TABLE_URL no longer appears to be valid (returns 404).
        This function will not work until it, or an alternate, is
        working.

    Args:
        symbol: Stock symbol (just one).
        start_date: Date format is 'YYYY-MM-DD'
        end_date: Date format is 'YYYY-MM-DD'

    Returns:
        Nested dictionary (dict of dicts); outer keys are dates in
        'YYYY-MM-DD' format.
    """
    params = urlencode({
        's': symbol,
        'a': int(start_date[5:7]) - 1,
        'b': int(start_date[8:10]),
        'c': int(start_date[0:4]),
        'd': int(end_date[5:7]) - 1,
        'e': int(end_date[8:10]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
        })
    url = '%s?%s' % (TABLE_URL, params)
    req = Request(url)
    resp = urlopen(req)
    content = str(resp.read().decode('utf-8').strip())
    daily_data = content.splitlines()
    hist_dict = dict()
    keys = daily_data[0].split(',')
    for day in daily_data[1:]:
        day_data = day.split(',')
        date = day_data[0]
        hist_dict[date] = {
            keys[1]: day_data[1],
            keys[2]: day_data[2],
            keys[3]: day_data[3],
            keys[4]: day_data[4],
            keys[5]: day_data[5],
            keys[6]: day_data[6],
            }
    return hist_dict
