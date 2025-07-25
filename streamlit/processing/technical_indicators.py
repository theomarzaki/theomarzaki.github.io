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
