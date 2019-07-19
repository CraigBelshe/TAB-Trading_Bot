import time
from datetime import datetime
import sqlite3
import logging
import sys

import requests

import constants
import utils
import settings


class MarketDataInterface:
    def __init__(self, market):
        self.market = market
        self.vwap = None
        self.volume = None
        self.value = None
        self.date = None
        self.buy_eur = None
        self.sell_eur = None
        self.bids = None
        self.asks = None
        self.order_cnt = 0

    # Retrieving from Database
    def get_ticker_data(self, previous):
        try:
            if previous is True:
                return utils.sql_fetch(
                    'SELECT * FROM ticker WHERE pair="{pair}" ORDER BY id DESC LIMIT 2'.format(pair=self.market)
                )[1]
            else:
                return utils.sql_fetch(
                    'SELECT * FROM ticker WHERE pair="{pair}" ORDER BY id DESC LIMIT 1'.format(pair=self.market)
                )[0]
        except sqlite3.DatabaseError:
            logging.info('getting ticker data failed')

    def get_all_ticker(self, num_amount):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE pair ="{pair}" ORDER BY id DESC LIMIT {amount}'
            .format(pair=self.market, amount=num_amount)
        )

    def get_order_book_asks(self):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE (type="ask" AND pair="{pair}")'.format(pair=self.market)
        )

    def get_order_book_bids(self):
        return utils.sql_fetch(
            'SELECT * FROM ticker WHERE (type="bid" AND pair="{pair}")'.format(pair=self.market)
        )

    # Updating Database
    def update_ticker(self):
        try:
            ticker = self.get_ticker()
            self.vwap = float(ticker['vwap'])
            self.volume = float(ticker['volume'])
            self.value = float(ticker['last'])
            self.date = datetime.fromtimestamp(float(ticker['timestamp']))

            utils.sql_exec(
                'INSERT INTO ticker (pair, date, value, volume, vwap) '
                'VALUES ("{pair}", "{date}", "{value}", "{volume}", "{vwap}")'
                .format(pair=self.market, date=self.date, value=self.value, volume=self.volume, vwap=self.vwap)
            )
            logging.info('ticker updated')

        except requests.exceptions.RequestException:
            logging.warning('request for ticker failed')

    def get_order_book(self):
        return requests.get(constants.BITSTAMP_API_ENDPOINT.format(command='order_book', market=self.market)).json()

    def get_ticker(self):
        return requests.get(constants.BITSTAMP_API_ENDPOINT.format(command='ticker', market=self.market)).json()

    def update_order_book(self):
        try:
            if self.order_cnt == settings.UPDATE_ORDER_FREQ:
                order_book = self.get_order_book()
                self.bids = order_book.get('bids', [])
                self.asks = order_book.get('asks', [])
                for bid in self.bids:
                    utils.sql_exec(
                        'INSERT INTO order_book (id, type, pair, price, amount)'
                        ' VALUES (NULL, "bid", "{pairs}", "{bid}", "{amount}");'
                        .format(pairs=self.market, bid=bid[0], amount=bid[1])
                    )

                for ask in self.asks:

                    utils.sql_exec(
                        'INSERT INTO order_book (id, type, pair, price, amount)'
                        ' VALUES (NULL, "ask", "{pairs}", "{ask}", "{amount}")'
                        .format(pairs=self.market, ask=ask[0], amount=ask[1])
                    )
                logging.info('order book updated')
                self.order_cnt = 0

            else:
                self.order_cnt += 1
                
        except requests.exceptions.RequestException:
            logging.warning('request for order book failed')

# Getting from exchange
    def get_transactions(self):
        transactions = requests.get(constants.BITSTAMP_API_TRANS + self.market)
        return transactions.json()

    def get_eur_usd(self):
        eur_usd = requests.get(constants.BITSTAMP_EUR_USD)
        convert = eur_usd.json()
        self.buy_eur = convert['buy']
        self.sell_eur = convert['sell']


def main(market):
    md = MarketDataInterface(market)
    logging.info("beginning md update loop")
    while True:
        md.update_ticker()
        md.update_order_book()
        time.sleep(settings.LOOP_TIME)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)
    main(sys.argv[1])
    logging.info("md update loop stopped")
