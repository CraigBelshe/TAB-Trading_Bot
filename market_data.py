import time
from datetime import datetime
import sqlite3

import requests

import constants


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

    def get_current_prev_ticker(self, pairs, past):

        if past is True:
            pass

        else:
            pass

    def get_all_ticker(self, pairs):
        pass
