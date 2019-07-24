from decimal import Decimal
import logging

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
            sums += Decimal(ticker[3])
            div += 1
        return Decimal(sums/div)

    def calc_stochastic(self, period):
        prices = []
        data = self.md.get_all_ticker(period)
        for tick in data:
            prices.append(Decimal(tick[3]))
        hi = max(prices)
        low = min(prices)
        last_ticker_value = self.md.get_ticker_data(False)
        c = Decimal(last_ticker_value[3])

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
        risk = Decimal(abs(long_mv_avg - short_mv_avg) / 20000)
        if risk > 0.1:
            risk = 0.1
        risk = risk * multiplier
        logging.info('ts: calculated dual mv avg, risk is {}'.format(risk))
        return risk

    def stochastic_indicator(self, period):
        stoc = self.calc_stochastic(period)
        if stoc < 20:
            risk = Decimal((20 - stoc)/200)
            multiplier = 1
        elif stoc > 80:
            risk = Decimal((stoc - 80)/200)
            multiplier = -1
        else:
            risk = Decimal(0)
            multiplier = 0
        if risk > 0.1:
            risk = 0.1
        risk = risk * multiplier
        logging.info('ts: calculated stochastic, risk is {}'.format(risk))
        return risk

    def get_final_strat(self):
        percent_risk = self.dual_mv_avg_indicator(50, 10)

        if percent_risk > 0.01:
            action = 'buy'
        elif percent_risk < -0.01:
            action = 'sell'
        else:
            action = 'wait'
        logging.info('ts: final strategy. risk is {}'.format(percent_risk))
        return {'risk': abs(percent_risk), 'action': action}
