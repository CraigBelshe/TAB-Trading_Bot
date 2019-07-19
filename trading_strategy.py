
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
        long_mv_avg = self.calc_mv_avg(long_period)
        short_mv_avg = self.calc_mv_avg(short_period)
        if short_mv_avg > long_mv_avg:
            multiplier = 1
        elif short_mv_avg < long_mv_avg:
            multiplier = -1
        else:
            multiplier = 0
        risk = abs(long_mv_avg - short_mv_avg) / 20000
        if risk > 0.1:
            risk = 0.1
            risk = risk * multiplier
        return risk

    def stochastic_indicator(self, period):
        stoc = self.calc_stochastic(period)

        if stoc < 20:
            risk = abs(20 - stoc)/200
            multiplier = 1
        elif stoc > 80:
            risk = (stoc - 80)/200
            multiplier = -1
        else:
            risk = 0
            multiplier = 0
        if risk > 0.1:
            risk = 0.1
        risk = risk * multiplier
        return risk

    def get_final_strat(self):
        risk_mv = self.dual_mv_avg_indicator(50, 10)
        risk_stoc = self.stochastic_indicator(100)

        percent_amount = (risk_mv + risk_stoc)/2

        if percent_amount > 0.01:
            action = 'buy'
        elif percent_amount < -0.01:
            action = 'sell'
        else:
            action = 'wait'
        return {'risk': abs(percent_amount), 'action': action}


om = TradingStrategy('btcusd')
print om.get_final_strat()
print om.stochastic_indicator(100)
print om.dual_mv_avg_indicator(50, 10)
