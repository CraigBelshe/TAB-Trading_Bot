import time
from datetime import datetime
import sqlite3

import requests

import constants


#
class MarketData:
    def __init__(self):
        self.vwap, self.volume, self.value, self.date, self.buy_eur, self.sell_eur, self.bids, self.asks\
            = None, None, None, None, None, None, None, None

    def get_ticker(self, pairs):
        ticker = (requests.get(constants.bitstamp_ticker_addr + pairs)).json()
        self.vwap = float(ticker[constants.vwap])
        self.volume = float(ticker[constants.volume])
        self.value = float(ticker[constants.value])
        self.date = datetime.fromtimestamp(float(ticker[constants.time]))

    def update_ticker_table(self, pairs):
        connection = sqlite3.connect(constants.database)
        cursor = connection.cursor()
        data = 'INSERT INTO ticker VALUES ("{pair}", "{date}", "{value}", "{volume}", "{vwap}")'.format(
            pair=pairs, date=self.date, value=self.value, volume=self.volume, vwap=self.vwap)
        cursor.execute(data)
        connection.commit()
        connection.close()

    def get_order_book(self, pairs):
        order_book_json = (requests.get(constants.bitstamp_order_addr + pairs))
        order_book = order_book_json.json()
        self.bids = order_book['bids']
        self.asks = order_book['asks']

    def update_order_book_table(self, pairs):
        connection = sqlite3.connect(constants.database)
        cursor = connection.cursor()
        for bid in self.bids:
            data = 'INSERT INTO order_book (type, pair, price, amount) VALUES ("bid", "{pairs}", "{bid}", "{amount}")' \
                .format(pairs=pairs, bid=bid[0], amount=bid[1])
            cursor.execute(data)
        for ask in self.asks:
            data = 'INSERT INTO order_book (type, pair, price, amount) VALUES ("ask", "{pairs}", "{ask}", "{amount}")' \
                .format(pairs=pairs, ask=ask[0], amount=ask[1])
            cursor.execute(data)
        connection.commit()
        connection.close()

    @staticmethod
    def get_transactions(pairs):
        transactions = requests.get(constants.bitstamp_all_trans + pairs)
        return transactions.json()

    def get_eur_usd(self):
        eur_usd = requests.get(constants.bitstamp_eur_usd)
        convert = eur_usd.json()
        self.buy_eur = convert['buy']
        self.sell_eur = convert['sell']


class MarketDataInterface:
    def __init__(self):
        pass

    def get_current_prev_ticker(self, pairs, past):

        if past is True:
            pass

        else:
            pass

    def get_all_ticker(self, pairs):
        pass

    def get_order_asks(self, pairs):
        pass

    def get_order_bids(self, pairs):
        pass
