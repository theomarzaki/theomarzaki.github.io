import pandas as pd
from decision.score_based import verdict
import ticker
from price_prediction import train, test, predict, data_manipulation
from price_prediction.networks.lstm import LSTMRegressor
from indicators import indicators
from datetime import datetime, timedelta

# TICKERS = ["XRP-USD", "BTC-USD", "ETH-USD", "SOL-USD"]
# KRAKEN_TICKERS = ["XRPUSD", "XBTUSD", "ETHUSD", "SOLUSD"]

TICKERS = ["BTC-USD"]
KRAKEN_TICKERS = ["XBTUSD"]

INPUT_DIM = 36

df = pd.read_csv('data/merged_indicators.csv')
current_time = datetime.utcnow()
start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
start_of_week_ahead = (current_time).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
df = df.drop_duplicates(subset=['Date'])
df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
df.set_index("Date", inplace=True)
print(df.tail(50))


# if __name__ == "__main__":
#     for yf_ticker, kraken_ticker in zip(TICKERS, KRAKEN_TICKERS):
#         print(F"Ticker: {yf_ticker}")
#         ticker.setTickers(yf_ticker, kraken_ticker)
#
#     indicators = indicators.Indicators(kwargs=ticker.getTickers())
#     indicators.make_technical_indicator()
#     indicators.make_market_indicator()
#     indicators.make_economic_indicator()
#
#     data_manipulation.manipulate_data()
#
#     model = LSTMRegressor(input_dim=INPUT_DIM)
#
#     # Train Model
#     train.train(model)
#
#     # Test Model
#     test.test(model)
#
#     # Make Predictions
#     predict.predict(model)
#
#     verdict = verdict.GiveVerdict(indicators)
#     verdict.to_csv('data/verdict.csv')
