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
            if previous:
                return utils.sql_fetch(
                    'SELECT * FROM ticker WHERE pair="{pair}" ORDER BY id DESC LIMIT 2'.format(pair=self.market)
                )[1]
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE pair="{pair}" ORDER BY id DESC LIMIT 1'.format(pair=self.market)
            )[0]
        except sqlite3.Error:
            logging.exception('failed to get last ticker from db')

    def get_all_ticker(self, limit):
        try:
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE pair ="{pair}" ORDER BY id DESC LIMIT {amount}'
                .format(pair=self.market, amount=limit)
            )
        except sqlite3.Error:
            logging.exception('failed to get ticker from db')

    def get_order_book_asks(self):
        try:
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE (type="ask" AND pair="{pair}")'.format(pair=self.market)
            )
        except sqlite3.Error:
            logging.exception('failed to get order book asks from db')

    def get_order_book_bids(self):
        try:
            return utils.sql_fetch(
                'SELECT * FROM ticker WHERE (type="bid" AND pair="{pair}")'.format(pair=self.market)
            )
        except sqlite3.Error:
            logging.exception('failed to get order book bids from db')

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

        except (requests.exceptions.RequestException, sqlite3.Error):
            logging.exception('update ticker failed')

    def get_order_book(self):
        try:
            return requests.get(constants.BITSTAMP_API_ENDPOINT.format(command='order_book', market=self.market)).json()
        except requests.exceptions.RequestException:
            logging.exception('failed to get order book from exchange')

    def get_ticker(self):
        try:
            return requests.get(constants.BITSTAMP_API_ENDPOINT.format(command='ticker', market=self.market)).json()
        except requests.exceptions.RequestException:
            logging.exception('failed to get ticker from exchange')

    def update_order_book(self):
        try:
            if self.order_cnt == settings.UPDATE_ORDER_FREQ:
                order_book = self.get_order_book()
                self.bids = order_book.get('bids', [])
                self.asks = order_book.get('asks', [])

                if not self.bids:
                    logging.warning('order book not updating, no bids found')
                    return
                if not self.asks:
                    logging.warning('order book not updating, no asks found')

                sql_bid = 'INSERT INTO order_book (id, type, pair, price, amount) VALUES'
                for bid in self.bids:
                    sql_bid = '{sql_bid} (NULL, "bid", "{pair}", "{bid}", "{amount}"),'\
                        .format(sql_bid=sql_bid, pair=self.market, bid=bid[0], amount=bid[1])

                sql_bid = '{};'.format(sql_bid[:-1])
                utils.sql_exec(sql_bid)

                sql_ask = 'INSERT INTO order_book (id, type, pair, price, amount) VALUES'
                for ask in self.asks:
                    sql_ask = '{sql_ask} (NULL, "ask", "{pair}", "{ask}", "{amount}"),'\
                        .format(sql_ask=sql_ask, pair=self.market, ask=ask[0], amount=ask[1])

                sql_ask = '{};'.format(sql_ask[:-1])
                utils.sql_exec(sql_ask)

                logging.info('order book updated')
                self.order_cnt = 0

            else:
                self.order_cnt += 1
                
        except (requests.exceptions.RequestException, sqlite3.Error):
            logging.exception('update order book failed')

# Getting from exchange
    def get_transactions(self):
        try:
            transactions = requests.get(constants.BITSTAMP_API_TRANS + self.market)
            return transactions.json()
        except requests.exceptions.RequestException:
            logging.exception('failed to get transactions from exchange')

    def get_eur_usd(self):
        try:
            convert = requests.get(constants.BITSTAMP_EUR_USD).json()
            self.buy_eur = convert['buy']
            self.sell_eur = convert['sell']
        except requests.exceptions.RequestException:
            logging.exception('failed to get eur_usd rate from exchange')


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
