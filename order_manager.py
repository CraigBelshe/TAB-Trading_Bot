import requests
import constants
import hmac
import hashlib
import time
import settings


class OrderManager:
    def __init__(self):
        pass

    def signature_gen(self):
        return signature

    def get_balance(self, currency):
        pass

    def check_order(self):
        return result, price, amount

    def buy(self, pair, price, risk):
        pass

    def sell(self, pair, price, risk):
        pass

    def buy_instant(self, pair, amount):
        pass

    def sell_instant(self, pair, amount):
        pass

    def cancel_all_orders(self):
        pass

    def cancel_order(self, id_num):
        pass

    def order_status(self, id_num):
        pass

    def find_open_orders(self, pair):
        pass

    def find_past_transactions(self, num_trans, pair):
        pass

    def buy_market(self, pair, amount):
        pass

    def sell_market(self, pair, amount):
        pass
