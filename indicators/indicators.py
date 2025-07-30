from datetime import datetime
import yfinance as yf
import pandas as pd
from indicators import technical_indicators, market_indicators, economic_indicators, risk_indicators, sentiment_indicators


class Indicators():

    def __init__(self, kwargs):
        self.TICKER = kwargs['TICKER']
        self.KRAKEN_TICKER = kwargs['KRAKEN_TICKER']

    def fetch_data(self, local):
        if local:
            self.historical_data = pd.read_csv('data/historical_data.csv')
            self.technical_indicator = technical_indicators.TechnicalIndicators(self.historical_data.copy(), self.TICKER)
            self.risk_indicator = risk_indicators.RiskIndicators(self.historical_data.copy())
        else:
            self.historical_data = yf.download(self.TICKER, start='2015-01-01', end=datetime.today().strftime('%Y-%m-%d'))
            self.historical_data.index = pd.to_datetime(self.historical_data.index)
            self.historical_data.columns = ['_'.join(col) for col in self.historical_data.columns]
            self.historical_data.columns = [col.split("_")[0] for col in self.historical_data.columns]
            self.historical_data.to_csv('data/historical_data.csv')
            self.technical_indicator = technical_indicators.TechnicalIndicators(self.historical_data.copy(), self.TICKER)
            self.risk_indicator = risk_indicators.RiskIndicators(self.historical_data.copy())

    def make_technical_indicator(self):
        technical_indicator = self.technical_indicator.calculate_technical_indicators()
        technical_indicator.to_csv('data/technical_indicators.csv')
        return technical_indicator

    def make_market_indicator(self):
        market_indicator = market_indicators.MarketIndicators(self.historical_data.copy(), self.KRAKEN_TICKER).calculate_market_indicators()
        market_indicator.to_csv('data/market_indicators.csv')
        return market_indicator

    def make_economic_indicator(self):
        economic_indicator = economic_indicators.EconomicIndicators(self.historical_data.copy()).calculate_economic_indicators()
        economic_indicator.to_csv('data/economic_indicators.csv')
        return economic_indicator

    def make_risk_indicators(self):
        risk_indicator = risk_indicators.RiskIndicators(self.historical_data.copy()).calculate_risk_indicators()
        risk_indicator.to_csv('data/risk_indicators.csv')
        return risk_indicator

    def make_sentiment_indicators(self):
        sentiment_indicator = sentiment_indicators.SentimentIndicators(self.historical_data.copy()).calculate_sentiment_indicators()
        sentiment_indicator.to_csv('data/sentiment_indicators.csv')
        return sentiment_indicator
