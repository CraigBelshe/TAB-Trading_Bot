from decimal import Decimal
import numpy as np
import scipy.optimize
import logging
import time
from datetime import datetime


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

    def calc_stochastic(self, period):
        data = self.md.get_all_ticker(period)

        prices = ([Decimal(x[3]) for x in data])
        hi = max(prices)
        low = min(prices)
        last_ticker_value = Decimal(str((self.md.get_ticker_data(False))[3]))

        return (last_ticker_value - low) / (hi - low) * 100

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
            risk = Decimal(str(settings.MAX_RISK * -1))
        elif (y[-1]) > 1.003 * int(current_value[3]):
            risk = Decimal(str(settings.MAX_RISK))
        else:
            risk = 0
        logging.info('calculated interpolation')

        print('inter_pred = {0}, current = {1}'.format(y[-1], current_value))
        return risk

    def get_final_strategy(self):
        #  percent_risk = self.stochastic_indicator(1440)
        percent_risk = self.interpolation_indicator(3, 15)
        #  percent_risk = self.interpolation_indicator(2, 20)

        try:
            if percent_risk > 0.001:
                action = 'buy'
            elif percent_risk < -0.001:
                action = 'sell'
            else:
                action = 'wait'
            logging.info('ts: final strategy. risk is {}'.format(percent_risk))
            return {'risk': abs(percent_risk), 'action': action}
        except TypeError:
            logging.exception('could not get final action in get_final_strategy')
            return {'risk': percent_risk, 'action': 'wait'}
