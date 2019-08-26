from datetime import datetime
import time
import matplotlib.pyplot as plt

from TAB_linear_inter.interpolation import FitCurve
from market_data import MarketDataInterface


# def interpolate_ticker(market, data_amount):
#     md = MarketDataInterface(market)
#     data = md.get_all_ticker(data_amount)
#     value = [t[3] for t in data]
#     timestamp = [time.mktime(datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').timetuple()) for t in data]
#
#     return best_fit_line(timestamp, value), timestamp, value
#
#
# interpolated_values, x, y = interpolate_ticker('btcusd', 20000)
# new_x = interpolated_values[0]
# new_y = interpolated_values[1]
# plt.plot(x, y)
# plt.plot(new_x, new_y)
# plt.show()


def interpolate_ticker_curve(market, data_start, data_len, degree):
    md = MarketDataInterface(market)
    fc = FitCurve(degree)
    data = md.get_all_ticker(data_start)
    print(data)
    data_use = data[-data_len:]
    value = [t[3] for t in data]
    timestamp = [time.mktime(datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').timetuple()) - 1.5652e9 for t in data]

    value_use = [t[3] for t in data_use]
    timestamp_use = [time.mktime(datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').timetuple()) - 1.5652e9 for t in data_use]
    x, y = fc.best_fit_curve(timestamp_use, value_use)
    plt.plot(x, y, color='red', linewidth=.3)
    plt.plot(timestamp, value, color='blue', linewidth=0.1, markersize=6)
    plt.axvline(x=timestamp_use[0], linewidth=0.5, linestyle=':', color='purple')
    plt.savefig('figure_one.pdf', dpi=1000)
    plt.show()

    return x, y


x, y = interpolate_ticker_curve('btcusd', 90, 5, 2)
print(y[-1])
