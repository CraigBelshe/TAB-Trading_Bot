import hmac
import hashlib
import time

import requests

import settings
import constants


class OrderManager:
    def __init__(self, market):
        self.customer_id = settings.CUSTOMER_ID
        self.api_key = settings.API_KEY
        self.api_secret = settings.API_SECRET
        self.nonce = time.time()
        self.order = {}
        self.market = market

    def signature_gen(self):
        self.nonce = str(int(time.time()))
        message = self.nonce + self.customer_id + self.api_key
        signature = hmac.new(
            self.api_secret,
            msg=message,
            digestmod=hashlib.sha256).hexdigest().upper()
        return signature

    def get_balance(self):
        sig = self.signature_gen()
        balance_data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce}
        account_balance = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='balance', market=self.market)),
                                        data=balance_data)
        account = account_balance.json()
        currency = self.market[-3:]
        balance = account[currency + '_balance']
        available = account[currency + '_available']
        reserved = account[currency + '_reserved']
        account_balance = {'balance': balance, 'available': available, 'reserved': reserved}
        return account_balance

    def check_order(self):
        if self.order['status'] != 'error':
            result = True
            price = self.order['price']
            amount = self.order['amount']
        else:
            result = False
            price = 0
            amount = 0
        return [result, price, amount]

    def buy(self, price, risk):
        balance = self.get_balance()

        amount = balance['available'] * risk / price
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount, 'price': price}
        buy_limit_order = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy', market=self.market)),
                                        data=data)
        self.order = buy_limit_order.json()

        return self.check_order()

    def sell(self, price, risk):
        balance = self.get_balance()

        amount = balance['available'] * risk
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount, 'price': price}
        sell_limit_order = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell', market=self.market)),
                                         json=data)
        self.order = sell_limit_order.json()

        return self.check_order()

    def buy_instant(self, amount):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount}
        buy_inst = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy/instant', market=self.market)),
                                 json=data)
        self.order = buy_inst.json()

        return self.check_order()

    def sell_instant(self, amount):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount}
        sell_inst = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell/instant', market=self.market)),
                                  json=data)
        self.order = sell_inst.json()

        return self.check_order()

    def cancel_all_orders(self):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce}
        cancel_ord = requests.post((constants.BITSTAMP_API_ONE.format(command='cancel_all_orders')),
                                   json=data)
        res = cancel_ord.json()
        return res

    def cancel_order(self, id_num):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'id': id_num}
        cancel_ord = requests.post(constants.BITSTAMP_API_NM.format(command='cancel_order'), json=data)
        return cancel_ord.json()

    def order_status(self, id_num):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'id': id_num}
        ord_status = requests.post(constants.BITSTAMP_API_ONE.format(command='order_status'), json=data)
        return ord_status.json()

    def find_open_orders(self):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce}
        open_orders = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='open_orders', market=self.market)),
                                    json=data)
        return open_orders.json()

    def find_past_transactions(self, num_trans):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'limit': num_trans}
        past_trans = requests.post((constants.BITSTAMP_API_ENDPOINT(command='user_transactions', market=self.market)),
                                   json=data)
        return past_trans

    def buy_market(self, amount):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount}
        buy_market = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy/market', market=self.market)),
                                   json=data)
        self.order = buy_market.json()

        return self.check_order()

    def sell_market(self, amount):
        sig = self.signature_gen()
        data = {'key': self.api_key, 'signature': sig, 'nonce': self.nonce, 'amount': amount}
        sell_market = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell/market', market=self.market)),
                                    json=data)
        self.order = sell_market.json()

        return self.check_order()
