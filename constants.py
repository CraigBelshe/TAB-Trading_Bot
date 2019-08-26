from enum import Enum

ORDER_STATUS_FINISHED = 'finished'
ORDER_STATUS_OPEN = 'open'
ORDER_STATUS_QUEUE = 'queue'
MARKETS = ['btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur',
           'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc', 'ethusd',
           'etheur', 'ethbtc', 'bchusd', 'bcheur', 'bchbtc']
EUR_USD_MIN = 25
BTC_MIN = .001


class BitstampAPI(Enum):
    # endpoint = 'https://www.bitstamp.net/api/v2/{command}/{market}/'
    # one = 'https://www.bitstamp.net/api/{command}/'
    # no_market = 'https://www.bitstamp.net/api/v2/{command}/'
    # transactions = 'https://www.bitstamp.net/api/v2/transactions/{market}'
    # eur_usd = 'https://www.bitstamp.net/api/eur_usd/'
    endpoint = 'https://front.qa.stagebts.net/api/v2/{command}/{market}/'
    one = 'https://front.qa.stagebts.net/api/{command}/'
    no_market = 'https://front.qa.stagebts.net/api/v2/{command}/'
    transactions = 'https://front.qa.stagebts.net/api/v2/transactions/{market}'
    eur_usd = 'https://front.qa.stagebts.net/api/eur_usd/'
