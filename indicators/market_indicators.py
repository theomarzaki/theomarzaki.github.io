import pandas as pd
from api import depth, spreads, sentiment


class MarketIndicators():

    def __init__(self, historical_data, ticker):
        self.ticker = ticker
        self.historical_data = historical_data

    # Function to calculate Market Cap
    def calculate_market_cap(self, df, circulating_supply_col='circulating_supply'):
        """
        Market Cap = Price * Circulating Supply
        """
        df['market_cap'] = df['Close'] * df[circulating_supply_col]
        return df

    # Function to calculate Liquidity (Bid-Ask Spread)
    def calculate_liquidity(self, df, bid_col='bid', ask_col='ask'):
        """
        Liquidity is measured by the Bid-Ask Spread.
        Spread = Ask Price - Bid Price
        """
        df['bid_ask_spread'] = df[ask_col] - df[bid_col]
        return df

    # Function to calculate Order Book Depth
    def calculate_order_book_depth(self, df, bid_volume_col='bid_volume', ask_volume_col='ask_volume'):
        """
        Order Book Depth = Total Bid Volume + Total Ask Volume
        """
        df['order_book_depth'] = df[bid_volume_col] + df[ask_volume_col]
        return df

    # Function to calculate Volume-Weighted Average Price (VWAP)
    def calculate_vwap(self, df):
        """
        VWAP = (Cumulative (Price * Volume)) / (Cumulative Volume)
        """
        df['cumulative_price_volume'] = (df['Close'] * df['Volume']).cumsum()
        df['cumulative_volume'] = df['Volume'].cumsum()
        df['vwap'] = df['cumulative_price_volume'] / df['cumulative_volume']
        return df

    # Function to calculate Network Value to Transactions (NVT) Ratio
    def calculate_nvt_ratio(self, df, transaction_volume_col='transaction_volume'):
        """
        NVT Ratio = Market Cap / Transaction Volume
        """
        df['nvt_ratio'] = df['market_cap'] / df[transaction_volume_col]
        return df

    # Function to calculate Whale Activity (Large Transactions)
    def calculate_whale_activity(self, df, large_transaction_threshold=1000000):
        """
        Whale Activity = Number of Transactions > Threshold
        """
        df['whale_activity'] = df['transaction_volume'].apply(
            lambda x: 1 if x > large_transaction_threshold else 0
        ).cumsum()
        return df

    # Global function to calculate all market indicators
    def calculate_market_indicators(self):

        ticker_spread = spreads.GetSpread(self.ticker)
        ticker_depth = depth.GetOrderBook(self.ticker)
        # sentiment_analysis = sentiment.fetchSentiment()
        #
        # merged_data = sentiment_analysis.join(self.historical_data, how='left')
        # print(merged_data.head())
        # print(merged_data.columns)
        # exit()

        merged_data = ticker_depth.join(self.historical_data, how='left')

        # Forward fill the ask and bid volumes to fill in missing timestamps
        merged_data[['ask_volume', 'bid_volume']] = merged_data[['ask_volume', 'bid_volume']].ffill()

        merged_data = ticker_spread.join(merged_data, how='left')

        # Drop rows where BTC data is missing (if any)
        merged_data.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)

        merged_data[merged_data.columns] = merged_data[merged_data.columns].apply(pd.to_numeric)

        # # Calculate Market Cap
        # df = self.calculate_market_cap(self.df)

        # Calculate Liquidity (Bid-Ask Spread)
        df = self.calculate_liquidity(merged_data)

        # Calculate Order Book Depth
        df = self.calculate_order_book_depth(df)

        # Calculate VWAP
        df = self.calculate_vwap(df)

        # Calculate NVT Ratio
        # df = self.calculate_nvt_ratio(df)

        # Calculate Whale Activity
        # df = self.calculate_whale_activity(df)

        return df
