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

        # Compute daily returns
        df['Return'] = df[price_col].pct_change()

        def rolling_cvar(series, alpha=0.95):
            series = series.dropna()
            if len(series) == 0:
                return np.nan
            var = np.percentile(series, (1 - alpha) * 100)
            cvar = series[series <= var].mean()
            return cvar

        df['CVaR'] = df['Return'].rolling(window).apply(rolling_cvar, raw=False)

        return df

    def calculate_risk_indicators(self):
        df = self.historical_data

        return self.compute_cvar_series(df)

    def update_risk_indicators(self):

        df = pd.read_csv('data/merged_indicators.csv')

        df.drop(columns=['CVaR'], inplace=True)

        current_time = datetime.utcnow()

        last_month = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
        df = df[(df['Date'] > last_month)]

        df = self.compute_cvar_series(df.copy())

        df.ffill(inplace=True)
        df.bfill(inplace=True)
        df.to_csv('data/merged_indicators.csv')

        return df
