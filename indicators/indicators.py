from datetime import datetime
import yfinance as yf
import pandas as pd
from indicators import technical_indicators, market_indicators, economic_indicators


class Indicators():

    def __init__(self, kwargs):
        self.TICKER = kwargs['TICKER']
        self.KRAKEN_TICKER = kwargs['KRAKEN_TICKER']
        self.historical_data = yf.download(self.TICKER, start='2020-01-01', end=datetime.today().strftime('%Y-%m-%d'))
        self.historical_data.index = pd.to_datetime(self.historical_data.index)
        self.historical_data.columns = ['_'.join(col) for col in self.historical_data.columns]
        self.historical_data.columns = [col.split("_")[0] for col in self.historical_data.columns]

    def technical_indicator(self):
        return technical_indicators.TechnicalIndicators(self.historical_data.copy(), self.TICKER).calculate_technical_indicators()

    def market_indicator(self):
        return market_indicators.MarketIndicators(self.historical_data.copy(), self.KRAKEN_TICKER).calculate_market_indicators()

    def economic_indicator(self):
        return economic_indicators.EconomicIndicators(self.historical_data.copy()).calculate_economic_indicators()
