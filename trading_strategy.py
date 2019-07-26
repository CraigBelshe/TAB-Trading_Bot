from decimal import Decimal
import logging

from market_data import MarketDataInterface


class TradingStrategy:
    def __init__(self, pair):
        self.pair = pair
        self.md = MarketDataInterface(pair)

    def calc_mv_avg(self, period):
        data = self.md.get_all_ticker(period)
        sums = Decimal(sum([x[3] for x in data]))
        div = len(data)
        return Decimal(sums/div)

    def calc_stochastic(self, period):
        data = self.md.get_all_ticker(period)

        prices = ([Decimal(x[3]) for x in data])
        hi = max(prices)
        low = min(prices)
        last_ticker_value = Decimal((self.md.get_ticker_data(False))[3])

        return (last_ticker_value - low) / (hi - low) * 100

    def dual_mv_avg_indicator(self, long_period, short_period):
        long_mv_avg = self.calc_mv_avg(long_period)
        short_mv_avg = self.calc_mv_avg(short_period)
        if short_mv_avg > long_mv_avg:
            multiplier = 1
        elif short_mv_avg < long_mv_avg:
            multiplier = -1
        else:
            multiplier = 0
        risk = Decimal(abs(long_mv_avg - short_mv_avg) / 20000)
        if risk > 0.1:
            risk = 0.1
        risk = risk * multiplier
        logging.info('ts: calculated dual mv avg, risk is {}'.format(risk))

        return risk

    def stochastic_indicator(self, period):
        stochastic = self.calc_stochastic(period)
        if stochastic < 20:
            risk = Decimal((20 - stochastic)/200)
            multiplier = 1
        elif stochastic > 80:
            risk = Decimal((stochastic - 80)/200)
            multiplier = -1
        else:
            risk = Decimal(0)
            multiplier = 0
        if risk > 0.1:
            risk = 0.1
        risk = risk * multiplier
        logging.info('ts: calculated stochastic, risk is {}'.format(risk))
        return risk

    def get_final_strategy(self):
        percent_risk = self.dual_mv_avg_indicator(50, 10)

        if percent_risk > 0.01:
            action = 'buy'
        elif percent_risk < -0.01:
            action = 'sell'
        else:
            action = 'wait'
        logging.info('ts: final strategy. risk is {}'.format(percent_risk))
        return {'risk': abs(percent_risk), 'action': action}
