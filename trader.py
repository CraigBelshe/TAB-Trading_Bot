import sys
import logging

from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_data import MarketDataInterface
import constants

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)

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
    action = ts.get_final_strat()