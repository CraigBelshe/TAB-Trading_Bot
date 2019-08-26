from decimal import Decimal
from decimal import InvalidOperation
import logging
import time
from datetime import datetime

from market_data import MarketDataInterface
from TAB_linear_inter.interpolation import FitCurve
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

    def calc_slope(self, period):
        data = self.md.get_all_ticker(period)
        price_initial = Decimal(data[-1][3])
        time_initial = Decimal(time.mktime(datetime.strptime(data[-1][2], '%Y-%m-%d %H:%M:%S').timetuple()))
        price_final = Decimal(data[0][3])
        time_final = Decimal(time.mktime(datetime.strptime(data[0][2], '%Y-%m-%d %H:%M:%S').timetuple()))

        try:
            slope = (price_final - price_initial)/(time_final - time_initial)
            print(slope)
            return slope

        except InvalidOperation:
            logging.exception('could not calculate slope')
            return None

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

    def slope_indicator(self, period):
        try:
            slope = self.calc_slope(period)
            if slope < 0:
                multiplier = -1
            elif slope > 0:
                multiplier = 1
            else:
                multiplier = 0
            risk = abs(slope) / Decimal('2')

            risk = risk * Decimal('100')

            if risk > settings.MAX_RISK:
                risk = settings.MAX_RISK
            risk = risk * multiplier
            logging.info('ts: calculated slope, risk is {}'.format(risk))

            return risk

        except TypeError:
            return Decimal('0')

    def interpolation_indicator(self, degree, period):
        fc = FitCurve(degree)
        data = self.md.get_all_ticker(period)
        value = [t[3] for t in data]
        timestamp = [time.mktime(datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').timetuple()) - 1.5652e9 for t in data]
        x, y = fc.best_fit_curve(timestamp, value)
        current_value = self.md.get_ticker_data(False)
        if (y[-1]) < 0.997 * int(current_value[3]):
            risk = Decimal('-0.5')
        elif (y[-1]) > 1.003 * int(current_value[3]):
            risk = Decimal('0.5')
        else:
            risk = 0
        logging.info('calculated interpolation')

        print('inter_pred = {0}, current = {1}'.format(y[-1], current_value))
        return risk

    def get_final_strategy(self):
        # percent_risk = self.dual_mv_avg_indicator(10, 5)
        # percent_risk = self.slope_indicator(8)
        percent_risk = self.interpolation_indicator(4, 800)
        #  percent_risk = 1000 * percent_risk

        if percent_risk > 0.001:
            action = 'buy'
        elif percent_risk < -0.001:
            action = 'sell'
        else:
            action = 'wait'
        logging.info('ts: final strategy. risk is {}'.format(percent_risk))
        return {'risk': abs(percent_risk), 'action': action}
