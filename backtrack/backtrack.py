from backtesting.lib import FractionalBacktest
from backtrack.lstm import LSTMStrategy
from backtrack.dca import DCAStrategy
import pandas as pd
from bokeh.plotting import output_file, save
import json


class BackTestStrategies():

    def __init__(self):
        self.df = pd.read_csv('data/merged_indicators.csv', index_col=0)
        self.df['Date'] = pd.to_datetime(self.df['Date'])  # convert to datetime if needed
        self.df.set_index('Date', inplace=True)

    def backtest_dca(self):
        initial_cash = 10000
        bt = FractionalBacktest(self.df, DCAStrategy, cash=10_000, commission=0.001, finalize_trades=True)
        stats = bt.run()

        final_equity = stats['Equity Final [$]']
        pnl = final_equity - initial_cash
        pnl_pct = stats['Return [%]']

        print(f"Initial Cash: ${initial_cash:,.2f}")
        print(f"Final Equity: ${final_equity:,.2f}")
        print(f"PnL: ${pnl:,.2f}")
        print(f"Return: {pnl_pct:.2f}%")

        print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
        print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
        print(f"Trades: {int(stats['# Trades'])}")

        plot = bt.plot()  # this returns a Bokeh layout
        output_file("backtrack/plots/backtest_dca.html")
        save(plot)

        summary = {
            "Initial Cash": 10_000,
            "Final Equity": float(stats['Equity Final [$]']),
            "PnL": float(stats['Equity Final [$]'] - 10_000),
            "Return (%)": float(stats['Return [%]']),
            "Sharpe Ratio": float(stats['Sharpe Ratio']),
            "Max Drawdown (%)": float(stats['Max. Drawdown [%]']),
            "Win Rate (%)": float(stats['Win Rate [%]']),
            "Total Trades": int(stats['# Trades']),
        }

        with open("backtrack/summary/stats_dca.json", "w") as f:
            json.dump(summary, f, indent=2)
        return None

    def backtest_lstm(self):
        initial_cash = 10000
        bt = FractionalBacktest(self.df, LSTMStrategy, cash=10_000, commission=0.001, finalize_trades=True)
        stats = bt.run()

        final_equity = stats['Equity Final [$]']
        pnl = final_equity - initial_cash
        pnl_pct = stats['Return [%]']

        print(f"Initial Cash: ${initial_cash:,.2f}")
        print(f"Final Equity: ${final_equity:,.2f}")
        print(f"PnL: ${pnl:,.2f}")
        print(f"Return: {pnl_pct:.2f}%")

        print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
        print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
        print(f"Trades: {int(stats['# Trades'])}")

        plot = bt.plot()  # this returns a Bokeh layout
        output_file("backtrack/plots/backtest_lstm.html")
        save(plot)

        summary = {
            "Initial Cash": 10_000,
            "Final Equity": float(stats['Equity Final [$]']),
            "PnL": float(stats['Equity Final [$]'] - 10_000),
            "Return (%)": float(stats['Return [%]']),
            "Sharpe Ratio": float(stats['Sharpe Ratio']),
            "Max Drawdown (%)": float(stats['Max. Drawdown [%]']),
            "Win Rate (%)": float(stats['Win Rate [%]']),
            "Total Trades": int(stats['# Trades']),
        }

        with open("backtrack/summary/stats_lstm.json", "w") as f:
            json.dump(summary, f, indent=2)
