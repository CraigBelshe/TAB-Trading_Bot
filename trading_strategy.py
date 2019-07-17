from market_data import MarketDataInterface

class TradingStrategy:
    def __init__(self, pair):
        self.pair = pair

    def calc_mv_avg(self, period):
        md = MarketDataInterface(self.pair)
        data = md.get_all_ticker(period)
        sums = 0
        div = 1
        for ticker in data:
            sums += ticker['value']
            div += 1
        return sums/div

    def get_actions(self, prev_ticker, current_ticker):
        return actions

    def get_risk(self, prev_ticker, current_ticker):
        return percent_amount


