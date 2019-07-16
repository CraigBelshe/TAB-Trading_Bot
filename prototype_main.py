import logging
import time
import sys

from market_data import MarketDataInterface
from trading_strategy import TradingStrategy
from order_manager import OrderManager


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def main():

    try:
        pair = sys.argv[1]
    except IndexError:
        pair = str(raw_input("Please specify which currency pair to use."))

    running = True

    md = MarketDataInterface()
    ts = TradingStrategy(pair)
    om = OrderManager()

    while running:
        prev_ticker = md.get_current_prev_ticker(pair, True)
        current_ticker = md.get_current_prev_ticker(pair, False)
        actions = ts.get_actions(prev_ticker, current_ticker)
        risk = ts.get_risk(prev_ticker, current_ticker)
        price = current_ticker['value']

        for action in actions:
            if action == "buy":
                result, order_details = om.buy(pair=pair, risk=risk, price=price)
                if result:
                    logging.info('Successfully bought {0} at ${1}'.format(order_details['actual_amount'], order_details['actual_end_price']))
                else:
                    logging.info('Buy failed')

            elif action == "sell":
                result, order_details = om.sell(pair=pair, risk=risk, price=price)
                if result:
                    logging.info('Successfully sold {0} at ${1}'.format(order_details['actual_amount'], order_details['actual_end_price']))
                else:
                    logging.info('Sell failed')

            elif action == "wait":
                result = True
                logging.info('Waited 10s, did not trade')

            else:
                running = False
                result = False
                logging.error('Unsupported action')

            return running, result

        time.sleep(settings.timer)


if __name__ == '__main__':
    main()
