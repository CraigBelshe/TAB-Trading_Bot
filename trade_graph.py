import csv
from datetime import datetime
import matplotlib.pyplot
import time

x = []
y = []
price = []

name_csvfile = str(input('enter file to use for balance (default: test_trading_balance.csv)'))
if not name_csvfile.endswith('csv'):
    print('default: test_trading_balance.csv')
    name_csvfile = 'test_trading_balance.csv'

with open(name_csvfile, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
#    market = plots[-1][5]
    for row in plots:
        z = time.mktime(datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f').timetuple())
        x.append(int(z))
        y.append((round(float(row[2]), 2)))
        price.append((round(float(row[4]), 5)))

fig, ax1 = matplotlib.pyplot.subplots()
colour = 'tab:red'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Total account balance (USD)', color=colour)
ax1.plot(x, y, color=colour)
ax1.tick_params(axis='y', labelcolor=colour)

ax2 = ax1.twinx()

colour = 'tab:blue'
# ax2.set_ylabel('Price of {currency_one} in {currency_two}'.format(currency_one=market[:3], currency_two=market[-3:]),
#                color=colour)
ax2.plot(x, price, color=colour)
ax2.tick_params(axis='y', labelcolor=colour)

fig.tight_layout()
matplotlib.pyplot.show()

# matplotlib.pyplot.plot(x, y, marker='o')
# matplotlib.pyplot.plot(x, price, marker='o')
# matplotlib.pyplot.xlabel('Time (s)')
# matplotlib.pyplot.ylabel('Total account balance (USD)')
# matplotlib.pyplot.title('Change in account value')
#
# matplotlib.pyplot.show()
