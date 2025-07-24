
# technical_indicators = {
#     "RSI": (34, "Oversold", "↑"),
#     "MACD": (-1.2, "Bearish", "↓"),
#     "MA Crossover": ("No", "Neutral", "→")
# }


def getTechnicalIndicatorsFromDate(snapshot):
    snapshot = df.loc[selected_date]
    kpis = {
        "RSI": (snapshot['RSI_14'], "PlaceHolder"),
        "SMA": (snapshot['SMA_20'], "PlaceHolder"),
        "EMA": (snapshot['EMA_20'], "PlaceHolder"),
        "MACD": (snapshot['MACD_12_26'], "PlaceHolder"),


    }

    return kpis
