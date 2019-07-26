import logging
import time
import sys

from market_data import MarketDataInterface
from trading_strategy import TradingStrategy
from order_manager import OrderManager
import settings
import constants


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def main():

    try:
        market = sys.argv[1]
    except IndexError:
        market = 'not a currency pair'

    if market not in constants.MARKETS:
        while True:
            market = str(input("Please specify which currency pair to use (btcusd, ltcusd, etc)."))
            if market in constants.MARKETS:
                break

    running = True

    md = MarketDataInterface(market)
    ts = TradingStrategy(market)
    om = OrderManager(market)

    while running:
        action = ts.get_final_strategy()
        price = (md.get_ticker_data(False))['value']
        order_details = om.get_order_status(id)

        if action['action'] == "buy":
            result = om.buy(pair=market, risk=action['risk'], price=price)
            order_details = om.get_order_status(result)
            if result[0]:
                logging.info('Successfully bought {0}{1} at {2}{3}'
                             .format(order_details['actual_amount'], market[:3], order_details['actual_end_price'], market[-3:]))
            else:
                logging.info('Buy failed')

        elif action['action'] == "sell":
            result = om.sell(pair=market, risk=action['risk'], price=price)
            order_details = om.get_order_status(result)
            if result:
                logging.info('Successfully sold {0}{1} at {2}{3}'
                             .format(order_details['amount'], market[:3], order_details['price'], market[-3:]))
            else:
                logging.info('Sell failed')

        elif action['action'] == "wait":
            logging.info('Waited {}s, did not trade'.format(settings.MAIN_TIMER))

        else:
            running = False
            logging.error('Unsupported action')

        time.sleep(settings.MAIN_TIMER)
        if not running:
            print('order error')


if __name__ == '__main__':
    main()
