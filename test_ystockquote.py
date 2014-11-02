#!/usr/bin/env python
"""
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

license: GNU LGPL

Requires: Python 2.7/3.3+
"""
__author__ = 'Corey Goldberg (cgoldberg@gmail.com)'
__copyright__ = 'Copyright (c) 2013 Corey Goldberg'
__version__ = '0.3.0'

import unittest

import pep8
from testscenarios import generate_scenarios, TestWithScenarios

import ystockquote

COMPANIES = {
    'GOOG': 'Google Inc.',
    'AAPL': 'Apple Inc.',
    }


class Pep8ConformanceTestCase(unittest.TestCase):
    """Test that all code conforms to PEP8!"""

    def test_pep8_conformance(self):
        self.pep8style = pep8.StyleGuide(show_source=True)
        files = ('ystockquote.py', 'test_ystockquote.py')
        self.pep8style.check_files(files)
        self.assertEqual(self.pep8style.options.report.total_errors, 0)


class YStockQuoteTestCase(TestWithScenarios):

    def test_get_all(self):
        test_inputs = (
            'GOOG',
            ('GOOG', 'AAPL')
            )
        for symbols in test_inputs:
            all_info = ystockquote.get_all(symbols)
            self.assertIsInstance(all_info, dict)
            if isinstance(symbols, str):
                symbols = [symbols]
            for symbol in symbols:
                check_value = all_info[symbol]['previous_close']
                self.assertNotEqual(check_value, 'N/A')
                self.assertGreater(float(check_value), 0)

    def test_get_tag(self):
        test_inputs = (
            ('GOOG', 'n'),
            ('GOOG', 'np'),
            (('GOOG', 'AAPL'), 'n'),
            (('GOOG', 'AAPL'), 'np'),
            )
        for symbols, tag_string in test_inputs:
            all_info = ystockquote.get_tag(symbols, tag_string)
            for symbol in all_info:
                self.assertEqual(all_info[symbol][0], COMPANIES[symbol])
                if len(all_info[symbol]) > 1:
                    self.assertNotEqual(all_info[symbol][1], 'N/A')

    def test_get_tags(self):
        test_inputs = (
            ('GOOG', 'previous_close'),
            ('GOOG', ('previous_close', 'company_name')),
            (('GOOG', 'AAPL'), 'previous_close'),
            (('GOOG', 'AAPL'), ('previous_close', 'company_name')),
            (('GOOG', 'AAPL'), ('p', 'company_name')),
            )
        for symbols, tags in test_inputs:
            all_info = ystockquote.get_tags(symbols, tags)
            self.assertIsInstance(all_info, dict)
            if isinstance(symbols, str):
                symbols = [symbols]
            if isinstance(tags, str):
                tags = [tags]
            for symbol in symbols:
                for tag in tags:
                    if tag == 'p':
                        tag = 'previous_close'
                    check_value = all_info[symbol][tag]
                    if tag == 'company_name':
                        self.assertEqual(check_value, COMPANIES[symbol])
                    else:
                        self.assertNotEqual(check_value, 'N/A')
                        self.assertGreater(float(check_value), 0)

#    def test_get_historical_prices(self):
#        symbol = 'GOOG'
#        start_date = '2013-01-02'
#        end_date = '2013-01-15'
#        prices = ystockquote.get_historical_prices(
#            symbol, start_date, end_date)
#        self.assertIsInstance(prices, dict)
#        self.assertEqual(len(prices), 10)
#        self.assertEqual(sorted(prices.keys())[0], '2013-01-02')
#        self.assertEqual(sorted(prices.keys())[-1], end_date)
#        self.assertGreater(float(prices[start_date]['Open']), 0.0)
#        self.assertGreater(float(prices[start_date]['High']), 0.0)
#        self.assertGreater(float(prices[start_date]['Low']), 0.0)
#        self.assertGreater(float(prices[start_date]['Close']), 0.0)
#        self.assertGreater(float(prices[start_date]['Volume']), 0.0)
#        self.assertGreater(float(prices[start_date]['Adj Close']), 0.0)
#        self.assertGreater(float(prices[end_date]['Open']), 0.0)
#        self.assertGreater(float(prices[end_date]['High']), 0.0)
#        self.assertGreater(float(prices[end_date]['Low']), 0.0)
#        self.assertGreater(float(prices[end_date]['Close']), 0.0)
#        self.assertGreater(float(prices[end_date]['Volume']), 0.0)
#        self.assertGreater(float(prices[end_date]['Adj Close']), 0.0)


if __name__ == '__main__':
    unittest.main()
