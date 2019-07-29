import logging
from time import sleep
from decimal import Decimal
import csv

from market_data import MarketDataInterface
from trading_strategy import TradingStrategy
from order_manager import OrderManager
import constants
import settings



with open('trade_record.csv', mode='w', newline='') as trades:
    tradewriter = csv.writer(trades, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    tradewriter.writerow()
