from backtesting.lib import FractionalBacktest
from backtrack.lstm import LSTMStrategy
import pandas as pd


class BackTestStrategies():

    def __init__(self):
        self.df = pd.read_csv('data/merged_indicators.csv', index_col=0)
        self.df['Date'] = pd.to_datetime(self.df['Date'])  # convert to datetime if needed
        self.df.set_index('Date', inplace=True)

    def backtest_lstm(self):
        bt = FractionalBacktest(self.df, LSTMStrategy, cash=10_000, commission=0.001)
        stats = bt.run()
        bt.plot()
