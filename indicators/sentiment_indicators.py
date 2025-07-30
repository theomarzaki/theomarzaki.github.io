import pandas as pd
import ta
from datetime import datetime, timedelta
import numpy as np
from api import sentiment


class SentimentIndicators():

    def __init__(self, df):
        self.historical_data = df

    def calculate_sentiment_indicators(self):

        sentiment_df = sentiment.fetchSentiment()

        self.historical_data = self.historical_data.reset_index()
        self.historical_data["Date"] = self.historical_data["Date"].astype("string")

        if 'index' in self.historical_data.columns:
            self.historical_data.drop(columns=['index'], inplace=True)

        sentiment_df = sentiment_df.reset_index()
        sentiment_df["Date"] = sentiment_df["Date"].astype("string")

        if 'index' in sentiment_df.columns:
            sentiment_df.drop(columns=['index'], inplace=True)

        df = pd.merge(sentiment_df, self.historical_data, on='Date', how='outer')

        # df = df.bfill()
        # df = df.ffill()

        return df
