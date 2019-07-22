from market_data import MarketDataInterface


class TradingStrategy:
    def __init__(self, pair):
        pass

    def calc_mv_avg(self, period):
        pass

    def get_actions(self, prev_ticker, current_ticker):
        pass

    def get_risk(self, prev_ticker, current_ticker):
        pass


