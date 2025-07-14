TICKER = "XRP-USD"
KRAKEN_TICKER = "XRPUSD"

kwargs = {'TICKER': TICKER, 'KRAKEN_TICKER': KRAKEN_TICKER}


def getTickers():
    return kwargs


def setTickers(TICKER, KRAKEN_TICKER):
    kwargs['TICKER'] = TICKER
    kwargs['KRAKEN_TICKER'] = KRAKEN_TICKER
