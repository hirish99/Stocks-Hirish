from backtesting import Backtest



def get_stats(start_date, end_date, data, cash, strategy):
    filtered_data = data[(data.index >= start_date)
                        & (data.index < end_date)]

    bt = Backtest(filtered_data, strategy, cash=cash, commission=.002,
                exclusive_orders=True)
    stats = bt.run()
    return stats
