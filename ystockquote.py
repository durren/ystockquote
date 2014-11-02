"""ystockquote : Retrieve stock quote data from Yahoo Finance

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

license: GNU LGPL

Requires: Python 2.7/3.3+
"""
__author__ = 'Corey Goldberg (cgoldberg@gmail.com)'
__contributor__ = 'Kevin (penniesfromkevin@gmail.com)'
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
    '1_year_target': 't8',
    '200_sma': 'm4',
    '50_sma': 'm3',
    '52_week_high': 'k',
    '52_week_low': 'j',
    '52_week_range': 'w',
    'after_hours_change': 'c8',
    'annualized_gain': 'g3',
    'ask_realtime': 'b2',
    'ask_size': 'a5',
    'average_daily_volume': 'a2',
    'bid_realtime': 'b3',
    'bid_size': 'b6',
    'book_value': 'b4',
    'change': 'c1',
    'change_200_sma': 'm5',
    'change_50_sma': 'm7',
    'change_from_52_week_high': 'k4',
    'change_from_52_week_low': 'j5',
    'change_percent': 'p2',
    'change_percent_change': 'c',
    'change_percent_realtime': 'k2',
    'change_realtime': 'c6',
    'commission': 'c3',
    'company_name': 'n',
    'dividend_pay_date': 'r1',
    'dividend_per_share': 'd',
    'dividend_yield': 'y',
    'ebitda': 'j4',
    'eps': 'e',
    'eps_estimate_current_year': 'e7',
    'eps_estimate_next_quarter': 'e9',
    'eps_estimate_next_year': 'e8',
    'ex_dividend_date': 'q',
    'float_shares': 'f6',
    'high_limit': 'l2',
    'holdings_gain': 'g4',
    'holdings_gain_percent': 'g1',
    'holdings_gain_percent_realtime': 'g5',
    'holdings_gain_realtime': 'g6',
    'holdings_value': 'v1',
    'holdings_value_realtime': 'v7',
    'last_trade_date': 'd1',
    'last_trade_price': 'l1',
    'last_trade_realtime_time': 'k1',
    'last_trade_size': 'k3',
    'last_trade_time': 't1',
    'last_trade_time_plus': 'l',
    'low_limit': 'l3',
    'market_cap': 'j1',
    'market_cap_realtime': 'j3',
    'more_info': 'v',
    'notes': 'n4',
    'order_book_realtime': 'i5',
    'pe': 'r',
    'pe_realtime': 'r2',
    'peg': 'r5',
    'percent_change_200_sma': 'm6',
    'percent_change_50_sma': 'm8',
    'percent_change_from_52_week_high': 'k5',
    'percent_change_from_52_week_low': 'j6',
    'previous_close': 'p',
    'price_book': 'p6',
    'price_eps_estimate_current_year': 'r6',
    'price_eps_estimate_next_year': 'r7',
    'price_paid': 'p1',
    'price_sales': 'p5',
    'revenue': 's6',
    'shares_outstanding': 'j2',
    'shares_owned': 's1',
    'short_ratio': 's7',
    'stock_exchange': 'x',
    'ticker_trend': 't7',
    'today_open': 'o',
    'todays_high': 'h',
    'todays_low': 'g',
    'todays_range': 'm',
    'todays_range_realtime': 'm2',
    'todays_value_change': 'w1',
    'todays_value_change_realtime': 'w4',
    'trade_date': 'd2',
    'trade_links': 't6',
    'volume': 'v',
    }


def _request(symbols, tag_string):
    """Makes the stock info request.

    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.
        tag_string: Tag or, confusingly, tag combination.
            Examples:
                'p1'   # single tag
                'np1v' # tag combination

    Returns:
        Dictionary with symbols as keys and list of tag values as
        values.
        {
            symbol1: [value1, .., valueN],
            ..
            symbolN: [value1, .., valueN],
            }
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    symbol_string = '+'.join(symbols)
    url = '%s?s=%s&f=%s' % (QUOTE_URL, symbol_string, tag_string)
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
    """Get all available quote data for the given ticker symbols.

    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.

    Returns:
        Dictionary of symbols with dictionary of tag values requested.
        See get_tags().
    """
    tags = SPECIAL_TAGS.keys()
    symbol_data = get_tags(symbols, tags)
    return symbol_data


def get_tag(symbols, tag_string):
    """Get tag values for multiple symbols.

    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.
        tag_string: Tag name, tag, or, confusingly, tag combination.
        Examples:
            'trade_date' # tag name
            'd2'         # tag
            'nd1d2'      # tag combination

    Returns:
        Dictionary of symbols with list of tag values requested.
        {
            symbol1: [value1, .., valueN],
            ..
            symbolN: [value1, .., valueN],
            }
    """
    if tag_string in SPECIAL_TAGS:
        tag_string = SPECIAL_TAGS[tag_string]
    return _request(symbols, tag_string)


def get_tags(symbols, tags):
    """Get multiple tag values for multiple symbols.

    This is similar to get_tag(), but a little more versatile with
    cleaner output (dictionary).

    Args:
        symbols: Stock symbol or, confusingly, list of stock symbols.
        tags: Tag name, tag, or, confusingly, list of tag names or tags.
            NOTE: Tag combination strings are no longer allowed.
        Examples:
            'trade_date' # tag name
            'd2'         # tag
            ['trade_date', 'd2'] # list of tag names and/or tags

    Returns:
        Dictionary of symbols with dictionary of tag values requested.
        {
            symbol1: {
                key1: value1,
                ..
                keyN: valueN,
                },
            ..
            symbolN: {
                key1: value1,
                ..
                keyN: valueN,
                },
            }
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    if isinstance(tags, str):
        tags = [tags]
    tag_parts = []
    tag_names = []
    for tag in tags:
        if tag in SPECIAL_TAGS:
            tag_names.append(tag)
            tag_parts.append(SPECIAL_TAGS[tag])
        elif tag in SPECIAL_TAGS.values():
            for tag_name, tag_abbr in SPECIAL_TAGS.items():
                if tag == tag_abbr:
                    tag_names.append(tag_name)
                    tag_parts.append(tag_abbr)
        else:
            # Handle unknown tags; pass value as tag
            tag_names.append('unknown')
            tag_parts.append(tag)
    tag_string = ''.join(tag_parts)
    symbol_data = _request(symbols, tag_string)
    symbol_dict = {}
    for symbol in symbols:
        symbol_dict[symbol] = {}
        for index, tag_name in enumerate(tag_names):
            symbol_dict[symbol][tag_name] = symbol_data[symbol][index]
    return symbol_dict


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
