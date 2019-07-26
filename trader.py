import sys
import logging
from time import sleep

from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_data import MarketDataInterface
import constants
import settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def main():

    try:
        market = sys.argv[1]
        if market not in constants.MARKETS:
            raise IndexError

    except IndexError:
        logging.info('need a market (btcusd, ltcusd, etc.)')
        while True:
            market = str(input("Please specify which currency pair to use (btcusd, ltcusd, etc)."))
            if market in constants.MARKETS:
                break

    logging.info('the market {} was chosen'.format(market))

    ts = TradingStrategy(market)
    om = OrderManager(market)
    md = MarketDataInterface(market)

    running = True

    while running:
        action = ts.get_final_strategy()
        price = (md.get_ticker_data(False))['value']
        balance = om.get_balance()

        if action['action'] == 'buy':
            amount = action['risk'] * balance['usd_available'] / price
        elif action['action'] == 'sell':
            amount = action['risk'] * balance['available']
        else:
            amount = 0

        if action['action'] == 'buy':
            order_id = om.buy(price=price, amount=amount)
            if order_id:
                logging.info('successfully bought {amount}{currency_one} at {price}{currency_two} each'
                             .format(amount=amount, currency_one=market[:3], price=price, currency_two=market[-3:]))

        elif action['action'] == 'sell':
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