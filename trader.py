from time import sleep
from decimal import Decimal
import sys
import logging
import argparse

from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_data import MarketDataInterface
import constants
import settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('market', type=str, choices=constants.MARKETS, help='currency pair - btcusd, ltcusd, etc')
    market = (parser.parse_args()).market

    logging.info('the market {} was chosen'.format(market))

    ts = TradingStrategy(market)
    om = OrderManager(market)
    md = MarketDataInterface(market)

    running = True

    while running:
        action = ts.get_final_strategy()
        price = Decimal(str((md.get_ticker_data(False))[3]))
        balance = om.get_balance()

        if action['action'] == 'buy':
            amount = action['risk'] * (Decimal(str(balance['usd_available'])) / Decimal(str(price)))
        elif action['action'] == 'sell':
            amount = action['risk'] * Decimal(str(balance['available']))
        else:
            amount = Decimal('0')

        if action['action'] in ['buy', 'sell']:
            if market[-3:] in ['usd', 'eur']:
                if (amount * price) < constants.EUR_USD_MIN_TRANSACTION_SIZE:
                    action['action'] = 'wait'
                    amount = Decimal('0')
                    logging.info('do not have minimum amount ({}) to trade'
                                 .format(constants.EUR_USD_MIN_TRANSACTION_SIZE))
                price = price.quantize(Decimal('.01'))

                if market[:3] in ['xrp', 'usd', 'eur']:
                    amount = amount.quantize(Decimal('.00001'))
                else:
                    amount = amount.quantize(Decimal('.00000001'))

            elif market[-3:] == 'btc':
                if (amount * price) < constants.BTC_MIN_TRANSACTION_SIZE:
                    action['action'] = 'wait'
                    amount = Decimal('0')
                    logging.info('do not have minimum amount ({}) to trade'
                                 .format(constants.BTC_MIN_TRANSACTION_SIZE))
                price = price.quantize(Decimal('.00000001'))

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
            logging.info('waited {}s, did not trade'.format(settings.MAIN_TIMER))

        else:
            running = False
            logging.error('Exiting Trader - unsupported action (supported actions: buy, sell, wait), {}'.format(action))

        sleep(settings.MAIN_TIMER)


if __name__ == '__main__':
    main()
