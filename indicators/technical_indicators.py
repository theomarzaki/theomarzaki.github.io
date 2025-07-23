import pandas as pd
import ta


class TechnicalIndicators():

    def __init__(self, df, ticker):
        self.historical_data = df
        self.ticker = ticker

    # Function to calculate Moving Averages (SMA and EMA)
    def calculate_moving_averages(self, df, period=20):
        df[f'SMA_{period}'] = ta.trend.SMAIndicator(df['Close'], window=period, fillna=True).sma_indicator()
        df[f'EMA_{period}'] = ta.trend.EMAIndicator(df['Close'], window=period, fillna=True).ema_indicator()
        return df

    # Function to calculate Relative Strength Index (RSI)
    def calculate_rsi(self, df, period=14):
        df[f'RSI_{period}'] = ta.momentum.RSIIndicator(df['Close'], window=period, fillna=True).rsi()
        return df

    # Function to calculate Bollinger Bands
    def calculate_bollinger_bands(self, df, period=20, std_dev=2):
        bbands = ta.volatility.BollingerBands(df['Close'], window=period, window_dev=std_dev, fillna=True)
        df = pd.concat([df, bbands.bollinger_hband(), bbands.bollinger_lband()], axis=1)
        return df

    # Function to calculate MACD
    def calculate_macd(self, df, fast_period=12, slow_period=26, signal_period=9):
        macd = ta.trend.MACD(df['Close'], window_fast=fast_period, window_slow=slow_period, window_sign=signal_period, fillna=True)
        df = pd.concat([df, macd.macd(), macd.macd_signal()], axis=1)
        return df

    # Function to calculate Stochastic Oscillator
    def calculate_stochastic_oscillator(self, df, k_period=14, d_period=3):
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=k_period, smooth_window=d_period, fillna=True)
        df = pd.concat([df, stoch.stoch()], axis=1)
        return df

    # Function to calculate On-Balance Volume (OBV)
    def calculate_obv(self, df):
        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume()
        return df

    # Function to calculate Ichimoku Cloud
    def calculate_ichimoku_cloud(self, df):
        ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'])
        df = pd.concat([df, ichimoku.ichimoku_a(), ichimoku.ichimoku_b()], axis=1)
        return df

    # Global function to calculate all technical indicators

    def calculate_technical_indicators(self):
        # Calculate Moving Averages
        df = self.calculate_moving_averages(self.historical_data.copy(), period=20)

        # Calculate RSI
        df = self.calculate_rsi(df, period=14)

        # Calculate Bollinger Bands
        df = self.calculate_bollinger_bands(df, period=20, std_dev=2)

        # Calculate MACD
        df = self.calculate_macd(df, fast_period=12, slow_period=26, signal_period=9)

        # Calculate Stochastic Oscillator
        df = self.calculate_stochastic_oscillator(df, k_period=14, d_period=3)

        # Calculate On-Balance Volume (OBV)
        df = self.calculate_obv(df)

        # Calculate Ichimoku Cloud
        df = self.calculate_ichimoku_cloud(df)

        return df

    def update_technical_indicators(self, df):
        # Calculate Moving Averages
        df = self.calculate_moving_averages(df, period=20)

        # Calculate RSI
        df = self.calculate_rsi(df, period=14)

        # Calculate Bollinger Bands
        df = self.calculate_bollinger_bands(df, period=20, std_dev=2)

        # Calculate MACD
        df = self.calculate_macd(df, fast_period=12, slow_period=26, signal_period=9)

        # Calculate Stochastic Oscillator
        df = self.calculate_stochastic_oscillator(df, k_period=14, d_period=3)

        # Calculate On-Balance Volume (OBV)
        df = self.calculate_obv(df)

        # Calculate Ichimoku Cloud
        df = self.calculate_ichimoku_cloud(df)

        return df
