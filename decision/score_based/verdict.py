from decision.score_based import technical, market, economic
from decision import start_of_week_previous, start_of_week_ahead
from decision.score_based import weights
import pandas as pd
import ticker
from indicators import indicators


def getWeightedVerdictFromScore(df, past_weight=1, future_weight=3):
    decision_map = {"Buy": 1, "Hold": 0, "Sell": -1}

    # Assume the first 3 rows are past, and the last 7 are future
    past_decisions = df.iloc[:3]['Decision'].map(decision_map)
    future_decisions = df.iloc[-7:]['Decision'].map(decision_map)

    # Apply weights
    weighted_past = past_decisions * past_weight
    weighted_future = future_decisions * future_weight

    # Aggregate weighted values
    total_score = weighted_past.sum() + weighted_future.sum()

    return total_score


def changeScoreToVerdict(score):
    if score > 0:
        return "Buy"
    elif score < 0:
        return "Sell"
    else:
        return "Hold"


def GiveVerdict():

    score_indicators = indicators.Indicators(kwargs=ticker.getTickers())

    technical_indicators = score_indicators.technical_indicator()
    market_indicators = score_indicators.market_indicator()
    economic_indicators = score_indicators.economic_indicator()

    technical_score = technical.make_decisions(technical_indicators).loc[start_of_week_previous:start_of_week_ahead]
    market_score = market.make_decisions(market_indicators).loc[start_of_week_previous:start_of_week_ahead]
    economic_score = economic.make_decisions(economic_indicators).loc[start_of_week_previous:start_of_week_ahead]

    technical_verdict = getWeightedVerdictFromScore(technical_score)
    market_verdict = getWeightedVerdictFromScore(market_score)
    economic_verdict = getWeightedVerdictFromScore(economic_score)

    verdict_df = pd.DataFrame(columns=['Indicator', 'Verdict'])
    verdict_df = pd.concat([pd.DataFrame([['Technical', changeScoreToVerdict(technical_verdict)]], columns=verdict_df.columns), verdict_df])
    verdict_df = pd.concat([pd.DataFrame([['Market', changeScoreToVerdict(market_verdict)]], columns=verdict_df.columns), verdict_df])
    verdict_df = pd.concat([pd.DataFrame([['Economic', changeScoreToVerdict(economic_verdict)]], columns=verdict_df.columns), verdict_df])

    total_score = technical_verdict * weights['Technical'] + market_verdict * weights['Market'] + economic_verdict * weights['Economic']

    verdict_df = pd.concat([pd.DataFrame([['Final', changeScoreToVerdict(total_score)]], columns=verdict_df.columns), verdict_df])
    verdict_df.set_index('Indicator')
    return verdict_df
