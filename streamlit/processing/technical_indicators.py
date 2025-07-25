
# technical_indicators = {
#     "RSI": (34, "Oversold", "↑"),
#     "MACD": (-1.2, "Bearish", "↓"),
#     "MA Crossover": ("No", "Neutral", "→")
# }


def getTechnicalIndicatorsFromDate(snapshot):
    kpis = {
        "RSI": (snapshot['RSI_14'], "PlaceHolder"),
        "SMA": (snapshot['SMA_20'], "PlaceHolder"),
        "EMA": (snapshot['EMA_20'], "PlaceHolder"),
        "MACD": (snapshot['MACD_12_26'], "PlaceHolder"),
    }

    return kpis


def rsi_comment(rsi):
    if rsi > 70:
        return "Overbought – Possible reversal"
    elif rsi < 30:
        return "Oversold – Potential rally"
    else:
        return "Neutral momentum"


def ma_comment(price, sma, ema):
    if price > sma and price > ema:
        return "Above MA – Bullish trend"
    elif price < sma and price < ema:
        return "Below MA – Bearish trend"
    else:
        return "Price near MA – indecisive"


def macd_comment(macd):
    if macd > 0:
        return "Positive MACD – Bullish bias"
    elif macd < 0:
        return "Negative MACD – Bearish bias"
    else:
        return "MACD near zero – Neutral momentum"
