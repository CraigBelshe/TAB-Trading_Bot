import hmac
import hashlib
import time
import logging

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

    def get_signature(self):  #
        self.nonce = str(int(time.time()))
        message = self.nonce + self.customer_id + self.api_key
        signature = hmac.new(
            self.api_secret,
            msg=message,
            digestmod=hashlib.sha256).hexdigest().upper()
        return {'key': self.api_key, 'signature': signature, 'nonce': self.nonce}

    def get_balance(self):  #
        data = self.get_signature()
        account = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='balance', market=self.market)),
                                data=data).json()
        currency = self.market[:-3]
        balance = account.get('{currency}_balance'.format(currency=currency))
        available = account.get('{currency}_available'.format(currency=currency))
        reserved = account.get('{currency}_reserved'.format(currency=currency))
        usd_available = account.get('usd_available')
        account_balance = {'balance': balance, 'available': available, 'reserved': reserved,
                           'usd_available': usd_available}
        return account_balance

    def buy(self, price, amount):  #

        data = self.get_signature()
        data.update({'amount': amount, 'price': price})
        buy_limit_order = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy', market=self.market)),
                                        data=data).json()
        if 'id' in buy_limit_order:
            return buy_limit_order['id']

        logging.info('buy order failed, {}'.format(buy_limit_order))
        return None

    def sell(self, price, amount):  #
        data = self.get_signature()
        data.update({'amount': amount, 'price': price})
        sell_limit_order = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell', market=self.market)),
                                         data=data).json()
        print sell_limit_order
        if 'id' in sell_limit_order:
            return sell_limit_order['id']

        logging.info('sell order failed, {}'.format(sell_limit_order))
        return None

    def instant_buy(self, amount):
        data = self.get_signature()
        data.update({'amount': amount})
        buy_inst = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy/instant', market=self.market)),
                                 data=data).json()
        if 'id' in buy_inst:
            return buy_inst['id']

        logging.info('instant buy order failed, {}'.format(buy_inst))
        return None

    def instant_sell(self, amount):
        data = self.get_signature()
        data.update({'amount': amount})
        sell_inst = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell/instant', market=self.market)),
                                  data=data).json()
        if 'id' in sell_inst:
            return sell_inst['id']

        logging.info('instant sell order failed, {}'.format(sell_inst))
        return None

    def cancel_all_orders(self):  #
        data = self.get_signature()
        cancel_order = requests.post((constants.BITSTAMP_API_ONE.format(command='cancel_all_orders')),
                                     data=data).json()
        if cancel_order is True:
            return cancel_order

        logging.info('failed to cancel all orders, {}'.format(cancel_order))
        return False

    def cancel_order(self, order_id):  #
        data = self.get_signature()
        data.update({'id': order_id})
        cancel_order = requests.post(constants.BITSTAMP_API_NM.format(command='cancel_order'), data=data).json()

        if 'id' in cancel_order:
            return True

        logging.info('failed to cancel order, {}'.format(cancel_order))
        return False

    def get_order_status(self, order_id):  #
        data = self.get_signature()
        data.update({'id': order_id})
        order_status = requests.post(constants.BITSTAMP_API_ONE.format(command='order_status'), data=data).json()
        if order_status.get('status') == 'Finished':
            return constants.ORDER_STATUS_FINISHED
        elif order_status.get('status') == 'Open':
            return constants.ORDER_STATUS_OPEN
        elif order_status.get('status') == 'In Queue':
            return constants.ORDER_STATUS_QUEUE
        else:
            logging.info('get order status failed, {}'.format(order_status))
            return None

    def get_open_orders(self):  #
        data = self.get_signature()
        open_orders = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='open_orders', market=self.market)),
                                    data=data).json()
        return open_orders

    def get_transactions(self, num_trans=100):  #
        data = self.get_signature()
        data.update({'limit': num_trans})
        past_trans = requests.post((constants.BITSTAMP_API_ENDPOINT
                                    .format(command='user_transactions', market=self.market)), data=data).json()
        return past_trans

    def market_buy(self, amount):
        data = self.get_signature()
        data.update({'amount': amount})
        buy_market = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='buy/market', market=self.market)),
                                   data=data).json()
        if 'id' in buy_market:
            return buy_market['id']

        logging.info('market buy failed, {}'.format(buy_market))
        return None

    def market_sell(self, amount):  #
        data = self.get_signature()
        data.update({'amount': amount})
        sell_market = requests.post((constants.BITSTAMP_API_ENDPOINT.format(command='sell/market', market=self.market)),
                                    data=data).json()
        if 'id' in sell_market:
            return sell_market['id']

        logging.info('market sell failed, {}'.format(sell_market))


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
market = 'btcusd'
om = OrderManager(market)

time.sleep(1)
print om.get_order_status(3797712719)

