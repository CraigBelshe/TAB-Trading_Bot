import sqlite3
import requests
from datetime import datetime
import constants
import time


#
class MarketData:
    def __init__(self):
        pass

    def update_ticker(self, pairs):
        pass

    def update_order_book(self, pairs):
        pass

    def get_transactions(self, pairs):
        pass

    def get_eur_usd(self):
        pass


class MarketDataInterface:
    def __init__(self):
        pass

    def get_current_ticker(self, pairs):
        pass

    def get_prev_ticker(self, pairs):
        pass

    def get_all_ticker(self, pairs):
        pass
