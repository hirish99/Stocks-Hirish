from backtesting import Backtest
from backtesting.test import GOOG

from sma_strategy1 import SmaCross

s = '2009-09-01'
f = '2011-09-15'
def get_stats(start_date, end_date, data, cash):
    filtered_data = data[(data.index >= s)
                        & (data.index < f)]

    bt = Backtest(filtered_data, SmaCross, cash=cash, commission=.002,
                exclusive_orders=True)
    stats = bt.run()
    return stats



stats = get_stats(s, f, GOOG, 10000)
print(stats)
print(stats['Return (Ann.) [%]'])