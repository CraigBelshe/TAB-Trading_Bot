import logging
import time
import sys

from market_data import MarketDataInterface
from trading_strategy import TradingStrategy
from order_manager import OrderManager
import settings


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def main():

    try:
        pair = sys.argv[1]
    except IndexError:
        pair = str(input("Please specify which currency pair to use."))

    running = True

    md = MarketDataInterface(pair)
    ts = TradingStrategy(pair)
    om = OrderManager(pair)

    while running:
        current_ticker = md.get_ticker_data(False)
        action = ts.get_final_strat()
        price = current_ticker['value']

        if action['action'] == "buy":
            result = om.buy(amount=action['risk'], price=price)
            if result[0]:
                logging.info('Successfully bought {0} at ${1}'.format(result[2], result[1]))
                result = True
            else:
                logging.info('Buy failed')
                result = False

        elif action['action'] == 'sell':
            result = om.sell(amount=action['risk'], price=price)
            if result[0]:
                logging.info('Successfully sold {0} at ${1}'.format(result[2], result[1]))
                result = True
            else:
                logging.info('Sell failed')
                result = False

        elif action['action'] == 'wait':
            result = True
            logging.info('Waited 10s, did not trade')

        else:
            running = False
            result = False
            logging.error('Unsupported action')

        time.sleep(settings.MAIN_TIMER)
        if not result:
            print('order error')


if __name__ == '__main__':
    main()
