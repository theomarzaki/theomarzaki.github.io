def get_inflation_adjusted_return_comment(value):
    if value > 0.01:
        return "Positive real return – bullish macro backdrop"
    elif value < -0.01:
        return "Negative real return – inflation drag"
    else:
        return "Neutral real return"


def get_real_interest_rate_comment(value):
    if value < 0:
        return "Negative real rates – supportive of risk assets"
    elif value < 1:
        return "Low real rates – mildly supportive"
    else:
        return "High real rates – bearish pressure"


def get_unemployment_rate_impact_comment(value):
    if value < -0.01:
        return "Improving labor market – bullish signal"
    elif value > 0.01:
        return "Rising unemployment – economic risk"
    else:
        return "Stable employment data"


def get_ppp_adjustment_comment(value):
    if value < 0.95:
        return "BTC undervalued by PPP – potential upside"
    elif value > 1.05:
        return "BTC overvalued by PPP – caution warranted"
    else:
        return "BTC fairly valued vs PPP"
