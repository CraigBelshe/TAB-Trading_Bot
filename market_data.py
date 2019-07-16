import time
from datetime import datetime
import sqlite3

import requests

import constants
import utils


class MarketDataInterface:
    def __init__(self, pairs):
        self.pairs = pairs
        self.vwap = None
        self.volume = None
        self.value = None
        self.date = None
        self.buy_eur = None
        self.sell_eur = None
        self.bids = None
        self.asks = None

# Retrieving from Database
    def get_ticker_data(self, previous):

        if previous is True:
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE pair="{pair}" AND ORDER BY id LIMIT 2'.format(pair=self.pairs)
            )[1]
        else:
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE pair="{pair}" AND ORDER BY id LIMIT 1'.format(pair=self.pairs)
            )[0]

    def get_all_ticker(self, num_amount):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE pair ="{pair}" AND ORDER BY id LIMIT {amount}'
            .format(pair=self.pairs, amount=num_amount)
        )

    def get_order_book_asks(self):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE (type="ask" AND pair="{pair}")'.format(pair=self.pairs)
        )

    def get_order_book_bids(self):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE (type="bid" AND pair="{pair}")'.format(pair=self.pairs)
        )

# Updating Database
    def update_ticker_table(self):
        utils.sql_exec(
            'INSERT INTO ticker VALUES ("{pair}", "{date}", "{value}", "{volume}", "{vwap}")'
            .format(pair=self.pairs, date=self.date, value=self.value, volume=self.volume, vwap=self.vwap)
        )

    def update_order_book_table(self):
        for bid in self.bids:
            utils.sql_exec(
                'INSERT INTO order_book (type, pair, price, amount) VALUES ("bid", "{pairs}", "{bid}", "{amount}")'
                .format(pairs=self.pairs, bid=bid[0], amount=bid[1])
            )

        for ask in self.asks:
            utils.sql_exec(
                'INSERT INTO order_book (type, pair, price, amount) VALUES ("ask", "{pairs}", "{ask}", "{amount}")'
                .format(pairs=self.pairs, ask=ask[0], amount=ask[1])
            )

# Getting from exchange
    def get_ticker(self):
        ticker = (requests.get(constants.bitstamp_ticker_addr + self.pairs))
        self.vwap = float(ticker[constants.vwap])
        self.volume = float(ticker[constants.volume])
        self.value = float(ticker[constants.value])
        self.date = datetime.fromtimestamp(float(ticker[constants.time]))

    def get_order_book(self):
        order_book_json = (requests.get(constants.bitstamp_order_addr + self.pairs))
        order_book = order_book_json.json()
        self.bids = order_book['bids']
        self.asks = order_book['asks']

    def get_transactions(self):
        transactions = requests.get(constants.bitstamp_all_trans + self.pairs)
        return transactions.json()

    def get_eur_usd(self):
        eur_usd = requests.get(constants.bitstamp_eur_usd)
        convert = eur_usd.json()
        self.buy_eur = convert['buy']
        self.sell_eur = convert['sell']


pair = 'btcusd'
i = 0
info = MarketDataInterface(pair)
while i < 10:
    info.get_ticker()
    info.get_order_book()
    info.update_ticker_table()
    info.update_order_book_table()
    time.sleep(10)
print info.get_ticker_data(True)
print info.get_ticker_data(False)
print info.get_order_book_asks()
print info.get_order_book_bids()
print info.get_all_ticker()