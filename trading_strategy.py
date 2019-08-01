from decimal import Decimal
from decimal import InvalidOperation
import logging

from market_data import MarketDataInterface
import settings


class TradingStrategy:
    def __init__(self, pair):
        self.pair = pair
        self.md = MarketDataInterface(pair)

    def calc_mv_avg(self, period):
        data = self.md.get_all_ticker(period)
        sums = Decimal(str(sum([x[3] for x in data])))
        div = len(data)
        try:
            return Decimal(str(sums/div))
        except InvalidOperation:
            logging.exception('could not calculate moving average, is there data in the database?')
            return 0

    def calc_stochastic(self, period):
        data = self.md.get_all_ticker(period)

        prices = ([Decimal(x[3]) for x in data])
        hi = max(prices)
        low = min(prices)
        last_ticker_value = Decimal(str((self.md.get_ticker_data(False))[3]))

        return (last_ticker_value - low) / (hi - low) * 100

    def dual_mv_avg_indicator(self, long_period, short_period):
        long_mv_avg = self.calc_mv_avg(long_period)
        short_mv_avg = self.calc_mv_avg(short_period)
        print(long_mv_avg, short_mv_avg)
        if short_mv_avg > long_mv_avg:
            multiplier = 1
        elif short_mv_avg < long_mv_avg:
            multiplier = -1
        else:
            multiplier = 0
        risk = Decimal(str(abs(long_mv_avg - short_mv_avg) / 500))
        if risk > settings.MAX_RISK:
            risk = settings.MAX_RISK
        risk = risk * multiplier
        logging.info('ts: calculated dual mv avg, risk is {}'.format(risk))

        return risk

    def stochastic_indicator(self, period):
        stochastic = self.calc_stochastic(period)
        if stochastic < 20:
            risk = Decimal(str((20 - stochastic)/200))
            multiplier = 1
        elif stochastic > 80:
            risk = Decimal(str((stochastic - 80)/200))
            multiplier = -1
        else:
            risk = Decimal('0')
            multiplier = 0
        if risk > settings.MAX_RISK:
            risk = settings.MAX_RISK
        risk = risk * multiplier
        logging.info('ts: calculated stochastic, risk is {}'.format(risk))
        return risk

    def get_final_strategy(self):
        percent_risk = self.dual_mv_avg_indicator(10, 5)

        if percent_risk > 0.001:
            action = 'buy'
        elif percent_risk < -0.001:
            action = 'sell'
        else:
            action = 'wait'
        logging.info('ts: final strategy. risk is {}'.format(percent_risk))
        return {'risk': abs(percent_risk), 'action': action}
