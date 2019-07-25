import sys
import logging

from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_data import MarketDataInterface

try:
    market = sys.argv[1]
    logging.info('the market {} was chosen'.format(market))

except IndexError:
    logging.error('need a market (btcusd, ltcusd, etc.)')
    exit()

ts = TradingStrategy(market)
om = OrderManager(market)
md = MarketDataInterface(market)