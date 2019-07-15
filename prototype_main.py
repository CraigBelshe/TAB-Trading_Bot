from market_data import MarketDataInterface
from trading_strategy import TradingStrategy
from order_manager import OrderManager
import logging
import time

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def main():

    market = sys.argv[1]

    running = True

    md = MarketDataInterface()
    ts = TradingStrategy(market)
    om = OrderManager()

    while running:
        prev_ticker = md.get_prev_ticker(market)
        current_ticker = md.get_current_ticker(market)
        actions = ts.get_actions(prev_ticker, current_ticker)
        risk = ts.get_risk(prev_ticker, current_ticker)
        price = current_ticker['value']

        for action in actions:
            if action == "buy":
                result, actual_end_price, actual_amount = om.buy(pair=market, risk=risk, price=price)
                if result:
                    logging.info('Successfully bought {0} at ${1}'.format(actual_amount, actual_end_price))
                else:
                    logging.info('Buy failed')

            elif action == "sell":
                result, actual_end_price, actual_amount = om.sell(pair=market, risk=risk, price=price)
                if result:
                    logging.info('Successfully sold {0} at ${1}'.format(actual_amount, actual_end_price))
                else:
                    logging.info('Sell failed')

            elif action == "wait":
                result = True
                logging.info('Waited 10s, did not trade')

            else:
                running = False
                result = False
                # raise Exception("Unsupported action")
                logging.error('Unsupported action')

            return running, result

        time.sleep(10)


if __name__ == '__main__':
    main()
