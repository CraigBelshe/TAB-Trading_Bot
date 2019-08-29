from decimal import Decimal
from decimal import InvalidOperation
from datetime import datetime
import numpy as np
import scipy.optimize
import time
import logging
import csv

from market_data import MarketDataInterface
import settings


class FitCurve:
    def __init__(self, degree):
        self.degree = degree

    # args are x value, then each coefficient in decreasing powers (y = ax^n + bx^n-1 + ... + cx^0)
    def func(self, *args):
        result = 0
        for i in range(self.degree + 1):
            result += (args[0]**i) * args[-1 * i - 1]

        return result

    def best_fit_curve(self, x, y):
        p0 = []
        for i in range(self.degree + 1):
            p0.append(1)
        values, unneeded = scipy.optimize.curve_fit(f=self.func, xdata=x, ydata=y, p0=p0, maxfev=100000)
        list_x = np.linspace(min(x), (max(x) + (max(x)-min(x)) * .1), 10000)
        return list_x, [self.func(xi, *values) for xi in list_x]


class TradingStrategy:
    def __init__(self, pair):
        self.pair = pair
        self.md = MarketDataInterface(pair)
        self.current_cross = None
        self.last_action = 'wait'

    def calc_mv_avg(self, period):
        data = self.md.get_all_ticker(period)

        sums = Decimal(str(sum([x[3] for x in data])))
        div = len(data)
        try:
            return Decimal(str(sums/div))
        except InvalidOperation:
            logging.exception('could not calculate moving average, is there data in the database?')
            return None

    def calc_slope(self, period):
        data = self.md.get_all_ticker(period)
        price_initial = Decimal(data[-1][3])
        time_initial = Decimal(time.mktime(datetime.strptime(data[-1][2], '%Y-%m-%d %H:%M:%S').timetuple()))
        price_final = Decimal(data[0][3])
        time_final = Decimal(time.mktime(datetime.strptime(data[0][2], '%Y-%m-%d %H:%M:%S').timetuple()))

        try:
            slope = (price_final - price_initial)/(time_final - time_initial)
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

        try:
            return (last_ticker_value - low) / (hi - low) * 100
        except InvalidOperation:
            logging.exception('could not calculate stochastic')
            return None

    def dual_mv_avg_indicator(self, long_period, short_period):
        long_mv_avg = self.calc_mv_avg(long_period)
        short_mv_avg = self.calc_mv_avg(short_period)
        if short_mv_avg > long_mv_avg:
            multiplier = 1
        elif short_mv_avg < long_mv_avg:
            multiplier = -1
        else:
            multiplier = 0
        risk = Decimal(str(abs(long_mv_avg - short_mv_avg) / 1000))
        if risk > settings.MAX_RISK:
            risk = settings.MAX_RISK
        risk = risk * multiplier
        logging.info('ts: calculated dual mv avg, risk is {}'.format(risk))

        return risk

    def cross_mv_avg_indicator(self, long_period, short_period):
        long_mv_avg = self.calc_mv_avg(long_period)
        short_mv_avg = self.calc_mv_avg(short_period)
        if not self.current_cross:
            if long_mv_avg > short_mv_avg:
                self.current_cross = 'sell'
            if long_mv_avg < short_mv_avg:
                self.current_cross = 'buy'

        if self.current_cross == 'sell':
            if long_mv_avg < short_mv_avg:
                self.current_cross = 'buy'
                risk = Decimal('0.2')
            else:
                risk = Decimal('0')

        elif self.current_cross == 'buy':
            if long_mv_avg > short_mv_avg:
                self.current_cross = 'sell'
                risk = Decimal('-0.2')
            else:
                risk = Decimal('0')
        else:
            risk = Decimal('0')

        return risk

    def differences_indicator(self, period):
        data = self.md.get_all_ticker(period)
        sums = data[0][3] - data[-1][3]
        risk = Decimal(sums / 100)
        while abs(risk) > .3:
            risk = risk/10
        return risk

    def past_performance_indicator(self, name_csvfile):
        with open(name_csvfile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            last_balance = lines[-1][2]
            prev_balance = lines[-2][2]
        print(last_balance, prev_balance)

        if self.last_action == 'wait':
            self.last_action = 'buy'
            risk = Decimal('1')
        elif Decimal(last_balance) < (Decimal('.997') * Decimal(prev_balance)):
            if self.last_action == 'sell':
                self.last_action = 'buy'
                risk = Decimal('1')
            elif self.last_action == 'buy':
                self.last_action = 'sell'
                risk = Decimal('-1')
            else:
                self.last_action = 'wait'
                risk = Decimal('0')
        elif Decimal(last_balance) > (Decimal('.997') * Decimal(prev_balance)):
            if self.last_action == 'sell':
                if (self.md.get_ticker_data(False))[3] < (self.md.get_ticker_data(True))[3]:
                    risk = Decimal('-1')
                else:
                    risk = Decimal('1')

            elif self.last_action == 'buy':
                risk = Decimal('1')
            else:
                self.last_action = 'wait'
                risk = Decimal('0')
        else:
            self.last_action = 'wait'
            risk = Decimal('0')

        return risk

    def slope_indicator(self, period):
        slope = self.calc_slope(period)
        if slope < 0:
            multiplier = -1
        elif slope > 0:
            multiplier = 1
        else:
            multiplier = 0
        risk = abs(slope) / Decimal('2')
        if risk > settings.MAX_RISK:
            risk = settings.MAX_RISK
        risk = risk * multiplier
        logging.info('ts: calculated slope, risk is {}'.format(risk))

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

    def interpolation_indicator(self, degree, period):
        fc = FitCurve(degree)
        data = self.md.get_all_ticker(period)
        value = [t[3] for t in data]
        timestamp = [time.mktime(datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').timetuple()) - 1.5652e9 for t in data]
        x, y = fc.best_fit_curve(timestamp, value)
        current_value = self.md.get_ticker_data(False)
        if (y[-1]) < 0.997 * int(current_value[3]):
            risk = Decimal('-1')
        elif (y[-1]) > 1.003 * int(current_value[3]):
            risk = Decimal('1')
        else:
            risk = 0
        logging.info('calculated interpolation')

        print('inter_pred = {0}, current = {1}'.format(y[-1], current_value))
        return risk

    def get_final_strategy(self):
        percent_risk = self.interpolation_indicator(3, 15)

        if percent_risk > 0.001:
            action = 'buy'
        elif percent_risk < -0.001:
            action = 'sell'
        else:
            action = 'wait'
        logging.info('ts: final strategy. risk is {}'.format(percent_risk))
        return {'risk': abs(percent_risk), 'action': action}