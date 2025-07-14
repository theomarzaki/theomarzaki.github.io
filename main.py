from decision.score_based import verdict
import ticker

TICKERS = ["XRP-USD", "BTC-USD", "ETH-USD", "SOL-USD"]
KRAKEN_TICKERS = ["XRPUSD", "XBTUSD", "ETHUSD", "SOLUSD"]


if __name__ == "__main__":
    for yf_ticker, kraken_ticker in zip(TICKERS, KRAKEN_TICKERS):
        print(F"Ticker: {yf_ticker}")
        ticker.setTickers(yf_ticker, kraken_ticker)
        print(verdict.GiveVerdict())
