import pandas as pd
from decision.score_based import verdict
import ticker
from price_prediction import train, test, predict, data_manipulation
from price_prediction.networks.lstm import LSTMRegressor
from indicators import indicators

# TICKERS = ["XRP-USD", "BTC-USD", "ETH-USD", "SOL-USD"]
# KRAKEN_TICKERS = ["XRPUSD", "XBTUSD", "ETHUSD", "SOLUSD"]

TICKERS = ["BTC-USD"]
KRAKEN_TICKERS = ["XBTUSD"]

INPUT_DIM = 36


if __name__ == "__main__":
    # for yf_ticker, kraken_ticker in zip(TICKERS, KRAKEN_TICKERS):
    #     print(F"Ticker: {yf_ticker}")
    #     ticker.setTickers(yf_ticker, kraken_ticker)

    indicators = indicators.Indicators(kwargs=ticker.getTickers())

    # data_manipulation.manipulate_data()

    # model = LSTMRegressor(input_dim=INPUT_DIM)

    # Train Model
    # train.train(model)

    # Test Model
    # test.test(model)

    # Make Predictions
    # predict.predict(model)

    verdict = verdict.GiveVerdict(indicators)
    # save suggestions
    verdict.to_csv('data/verdict.csv')
