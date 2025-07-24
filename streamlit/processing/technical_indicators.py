
# technical_indicators = {
#     "RSI": (34, "Oversold", "↑"),
#     "MACD": (-1.2, "Bearish", "↓"),
#     "MA Crossover": ("No", "Neutral", "→")
# }


def getTechnicalIndicatorsFromDate(snapshot):
    rsi = snapshot['RSI_14']
    sma = snapshot['SMA_20']
    ema = snapshot['EMA_20']
    macd = snapshot['MACD_12_26']
    kpis = {
        "RSI": (rsi, "PlaceHolder"),
        "SMA": (sma, "PlaceHolder"),
        "EMA": (ema, "PlaceHolder"),
        "MACD": (macd, "PlaceHolder"),
    }

    return kpis
