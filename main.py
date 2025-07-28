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


if __name__ == "__main__":
    for yf_ticker, kraken_ticker in zip(TICKERS, KRAKEN_TICKERS):
        print(F"Ticker: {yf_ticker}")
        ticker.setTickers(yf_ticker, kraken_ticker)

    indicators = indicators.Indicators(kwargs=ticker.getTickers())
    indicators.fetch_data(local=True)
    # indicators.make_technical_indicator()
    # indicators.make_market_indicator()
    # indicators.make_economic_indicator()
    #
    # data_manipulation.manipulate_data()
    #
    # model = LSTMRegressor(input_dim=INPUT_DIM)
    #
    # train.train(model)
    #
    # test.test(model)
    #
    # predict.predict(model)

    df = indicators.technical_indicator.update_technical_indicators()

    verdict = verdict.GiveVerdict(df.copy())
    verdict.to_csv('data/verdict.csv')
