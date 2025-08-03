import pandas as pd
import ta
from datetime import datetime, timedelta
import numpy as np


class RiskIndicators():

    def __init__(self, df):
        self.historical_data = df

    def calculate_var(self, returns):
        confidence_level = 0.95
        var = np.percentile(returns, (1 - confidence_level) * 100)
        return var

    def compute_cvar_series(self, df, price_col='Close', window=30, alpha=0.95):

        df['Return'] = df['Close'].pct_change()

        confidence_level = 0.95

        df['CVaR'] = df['Return'].rolling(window=30).apply(lambda x: x[x <= x.quantile(1 - confidence_level)].mean(), raw=False)

        return df

    def calculate_risk_indicators(self):
        df = self.historical_data

        return self.compute_cvar_series(df)

    def update_risk_indicators(self):

        df = pd.read_csv('data/merged_indicators.csv')

        df.drop(columns=['CVaR'], inplace=True)

        # current_time = datetime.utcnow()
        # last_month = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
        # df = df[(df['Date'] > last_month)]

        df = self.compute_cvar_series(df.copy())

        df.ffill(inplace=True)
        df.bfill(inplace=True)
        df.to_csv('data/merged_indicators.csv')

        return df
