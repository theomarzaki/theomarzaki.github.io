def obv_comment(obv, prev_obv):
    if obv > prev_obv:
        return "Increasing volume – trend confirmation"
    elif obv < prev_obv:
        return "Decreasing volume – possible weakening"
    else:
        return "Flat OBV – low conviction"


def vwap_comment(price, vwap):
    if price > vwap:
        return "Above VWAP – bullish bias"
    elif price < vwap:
        return "Below VWAP – bearish bias"
    else:
        return "Near VWAP – no clear signal"


def bid_ask_comment(spread):
    if spread < 5:  # adjust based on your instrument's scale
        return "Tight spread – liquid market"
    elif spread < 15:
        return "Moderate spread – cautious trading"
    else:
        return "Wide spread – illiquid or volatile"
