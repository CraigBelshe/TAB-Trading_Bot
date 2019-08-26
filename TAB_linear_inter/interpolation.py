import numpy as np
import scipy.optimize
from math import factorial
from scipy.signal import bsplines
import matplotlib.pyplot as plt


# def best_fit_line(x, y):
#     avg_x = sum(x) / len(x)
#     avg_y = sum(y) / len(y)
#
#     top = sum([(xi - avg_x) * (yi - avg_y) for xi, yi in zip(x, y)])
#     bottom = sum([(xi - avg_x)**2 for xi in x])
#     slope = top / bottom
#
#     y_intercept = avg_y - (slope * avg_x)
#     x_values = np.linspace((x[0] + 100000), x[-1], 3)
#     y_values = [slope * xi + y_intercept for xi in x_values]
#
#     return np.ndarray.tolist(x_values), y_values


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
        # plt.plot(list_x, [self.func(xi, *values) for xi in list_x], color='red')
        # plt.plot(x, y, color='blue')
        # plt.show()
        return list_x, [self.func(xi, *values) for xi in list_x]

    # def lagrange(self, x, y):
    #     k = len(x) - 1
    #     l = []
    #
    #     q = 1
    #     for m in range(k + 1):
    #         q = q



