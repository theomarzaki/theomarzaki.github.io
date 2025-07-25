def obv_comment(obv_diff):
    if obv_diff > 0:
        return "Increasing OBV – bullish volume momentum"
    elif obv_diff < 0:
        return "Decreasing OBV – bearish volume momentum"
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
