
from market_data import MarketDataInterface

class TradingStrategy:
    def __init__(self, pair):
        self.pair = pair
        self.md = MarketDataInterface(pair)

    def calc_mv_avg(self, period):
        data = self.md.get_all_ticker(period)
        sums = 0
        div = 0
        for ticker in data:
            sums += int(ticker[3])
            div += 1
        return float(sums/div)

    def calc_stochastic(self, period):
        prices = []
        data = self.md.get_all_ticker(period)
        for tick in data:
            prices.append(int(tick[3]))
        hi = max(prices)
        low = min(prices)
        data = self.md.get_ticker_data(False)
        c = data[3]

        return (c - low) / (hi - low) * 100

    def dual_mv_avg_indicator(self, long_period, short_period):
        self.long_mv_avg = self.calc_mv_avg(long_period)
        self.short_mv_avg = self.calc_mv_avg(short_period)
        if self.short_mv_avg > self.long_mv_avg:
            actions = 'buy'
        elif self.short_mv_avg < self.long_mv_avg:
            actions = 'sell'
        else:
            actions = 'wait'
        return actions

    def single_mv_avg_indicator(self, period):
        data = self.md.get_ticker_data(False)
        price = data[3]
        mv_avg = self.calc_mv_avg(period)
        if price > mv_avg:
            action = 'buy'
        elif price < mv_avg:
            action = 'sell'
        else:
            action = 'wait'
        return action

    def stochastic_indicator(self, period):
        self.stoc = self.calc_stochastic(period)
        if self.stoc < 20:
            action = 'buy'
        elif self.stoc > 80:
            action = 'sell'
        else:
            action = 'wait'
        return action

    def dual_mv_avg_risk(self):
        risk = abs(self.long_mv_avg - self.short_mv_avg)/20000
        if risk > 0.1:
            risk = 0.1
        return risk

    def stochastic_risk(self):
        if self.stoc < 20:
            risk = abs(20 - self.stoc)/200
        elif self.stoc > 80:
            risk = (self.stoc - 80)/200
        else:
            risk = 0
        if risk > 0.1:
            risk = 0.1
        return risk

    def get_final_action(self):
        actions = self.dual_mv_avg_indicator(15, 5)
        # actions = self.stochastic_indicator(15)
        return actions

    def get_final_risk(self):
        action_mv = self.dual_mv_avg_indicator(15, 5)
        action_stoc = self.stochastic_indicator(15)
        percent_amount_mv = self.dual_mv_avg_risk()
        percent_amount_stoc = self.stochastic_risk()

        if action_mv == 'sell':
            percent_amount_mv = -1*percent_amount_mv
        if action_stoc == 'sell':
            percent_amount_stoc = -1*percent_amount_stoc

        percent_amount = percent_amount_stoc + percent_amount_mv

        if percent_amount > 0:
            action = 'buy'
        elif percent_amount < 0:
            action = 'sell'
        else:
            action = 'wait'
        return {'risk': abs(percent_amount), 'action': action}

