from time import sleep
from decimal import Decimal
import sys
import logging
import datetime

from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_data import MarketDataInterface
import constants
import settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


def main():

    try:
        market = sys.argv[1]
        if market not in constants.MARKETS:
            raise IndexError

    except IndexError:
        logging.info('need a market (btcusd, ltcusd, etc.)')
        while True:
            market = str(input("Please specify which currency pair to use (btcusd, ltcusd, etc):"))
            if market in constants.MARKETS:
                break

    logging.info('the market {} was chosen'.format(market))

    ts = TradingStrategy(market)
    om = OrderManager(market)
    md = MarketDataInterface(market)

    running = True

    while running:
        action = ts.get_final_strategy()
        price = Decimal(str((md.get_ticker_data(False))[3]))

        time = datetime.datetime.now().timestamp()
        if abs(time - (datetime.datetime.strptime(md.get_ticker_data(False)[2], '%Y-%m-%d %H:%M:%S'))
                .timestamp()) > 600:
            logging.error('database is out of date, exiting')
            running = False

        balance = om.get_balance()
        if None in balance.values():
            logging.info('failed to get account balance')
        print(balance, action)
        print(price, action['risk'])

        try:
            if action['action'] == 'buy':
                amount = (Decimal(str(action['risk'])) * Decimal(balance['second_available']) / price)
            elif action['action'] == 'sell':
                amount = (Decimal(str(action['risk'])) * Decimal(balance['available']))
            else:
                amount = Decimal('0')
        except TypeError:
            logging.exception('could not determine amount')
            amount = Decimal('0')

        if market[-3:] in ['usd', 'eur']:
            if (amount * price) < constants.EUR_USD_MIN:
                action['action'] = 'wait'
                amount = Decimal('0')
                logging.info('do not have minimum amount ({}) to trade'.format(constants.EUR_USD_MIN))
        elif market[-3:] == 'btc':
            if (amount * price) < constants.BTC_MIN:
                action['action'] = 'wait'
                amount = Decimal('0')
                logging.info('do not have minimum amount ({}) to trade'.format(constants.BTC_MIN))

        amount = amount.quantize(Decimal('0.00000001'))
        price = price.quantize(Decimal('0.01'))

        if action['action'] == 'buy':
            sleep(1)
            order_id = om.buy(price=price, amount=amount)
            if order_id:
                logging.info('successfully bought {amount}{currency_one} at {price}{currency_two} each'
                             .format(amount=amount, currency_one=market[:3], price=price, currency_two=market[-3:]))

        elif action['action'] == 'sell':
            sleep(1)
            order_id = om.sell(price=price, amount=amount)
            if order_id:
                logging.info('successfully sold {amount}{currency_one} at {price}{currency_two} each'
                             .format(amount=amount, currency_one=market[:3], price=price, currency_two=market[-3:]))

        elif action['action'] == 'wait':
            logging.info('waiting {}s, did not trade'.format(settings.MAIN_TIMER))

        else:
            running = False
            logging.error('exiting Trader - unsupported action (supported actions: buy, sell, wait), {}'.format(action))

        sleep(1)
        open_orders = om.get_open_orders()
        if open_orders:
            for order in open_orders:
                time = datetime.datetime.now().timestamp()
                sleep(1)
                if datetime.datetime.strptime(order['datetime'], '%Y-%m-%d %H:%M:%S').timestamp() < time - 21600:
                    om.cancel_order(order['id'])

        sleep(settings.MAIN_TIMER)
        logging.info('waited {}s to trade again'.format(settings.MAIN_TIMER))


if __name__ == '__main__':
    main()
