import logging
from time import sleep
from datetime import datetime
from decimal import Decimal
import csv

from market_data import MarketDataInterface
from test_strategies import TradingStrategy
from order_manager import OrderManager
import constants
import settings


name_csvfile = str(input('enter file to use for balance (default: test_trading_balance.csv)'))
if not name_csvfile.endswith('csv'):
    print('default: test_trading_balance.csv')
    name_csvfile = 'test_trading_balance.csv'

with open(name_csvfile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    lines = list(reader)
    row = lines[-1]
csvfile.close()

balance_currency_one = Decimal(row[0])
balance_currency_two = Decimal(row[1])
market = row[2]
if market not in constants.MARKETS:
    while True:
        market = str(input("Please specify which currency pair to use (btcusd, ltcusd, etc):"))
        if market in constants.MARKETS:
            break

om = OrderManager(market)
ts = TradingStrategy(market)
md = MarketDataInterface(market)

while True:
    price = Decimal(str((md.get_ticker_data(False))[3]))
    action = ts.get_final_strategy()
    print(action)

    if action['action'] == 'buy':
        amount = Decimal(str(action['risk'])) * Decimal(str(balance_currency_two)) / Decimal(str(price))
    elif action['action'] == 'sell':
        amount = Decimal('-1') * Decimal(str((action['risk']))) * Decimal(str(balance_currency_one))
    else:
        amount = Decimal('0')

    if action['action'] in ['buy', 'sell']:
        if market[-3:] in ['usd', 'eur']:
            if abs(amount * price) < constants.EUR_USD_MIN_TRANSACTION_SIZE:
                action['action'] = 'wait'
                amount = Decimal('0')
                logging.info('do not have minimum amount ({}) to trade'.format(constants.EUR_USD_MIN_TRANSACTION_SIZE))
        elif market[-3:] == 'btc':
            if abs(amount * price) < constants.BTC_MIN_TRANSACTION_SIZE:
                action['action'] = 'wait'
                amount = Decimal('0')
                logging.info('do not have minimum amount ({}) to trade'.format(constants.BTC_MIN_TRANSACTION_SIZE))

    fee_one = Decimal('1')
    fee_two = Decimal('1')
    if action['action'] == 'buy':
        fee_one = Decimal('0.9975')
    elif action['action'] == 'sell':
        fee_two = Decimal('0.9975')

    balance_currency_one = balance_currency_one + (amount * fee_one)
    logging.info('bought {amount}{currency} at {price}{currency_two}'
                 .format(amount=amount, currency=market[:3], price=price, currency_two=market[:-3]))
    balance_currency_two = balance_currency_two - (amount * price * fee_two)
    logging.info('bought {amount}{currency} at {price}{currency_two}'
                 .format(amount=amount, currency=market[:3], price=price, currency_two=market[:-3]))

    total_balance_currency_two = (balance_currency_one * price) + balance_currency_two
    time = datetime.now()

    with open(name_csvfile, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')

        writer.writerow([balance_currency_one, balance_currency_two, total_balance_currency_two, time, price, market])

    print(balance_currency_one, balance_currency_two)
    sleep(settings.MAIN_TIMER)
