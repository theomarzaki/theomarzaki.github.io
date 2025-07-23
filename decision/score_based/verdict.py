from decision.score_based import technical, market, economic
from decision.score_based import weights
import pandas as pd
import ticker
from datetime import datetime, timedelta


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


def GiveVerdict(indicators):

    current_time = datetime.utcnow()

    df = pd.read_csv('data/merged_indicators.csv')

    last_month = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > last_month)]

    df.drop(columns=['SMA_20', 'EMA_20',
                     'RSI_14', 'hband', 'lband', 'MACD_12_26', 'MACD_sign_12_26', 'stoch_k',
                     'OBV', 'ichimoku_a_9_26', 'ichimoku_b_9_26'], inplace=True)

    df = indicators.technical_indicator.update_technical_indicators(df.copy())

    start_of_week = (current_time - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week)]
    df = df.drop_duplicates(subset=['Date'])

    technical_score = technical.make_decisions(df.copy())
    market_score = market.make_decisions(df.copy())
    economic_score = economic.make_decisions(df.copy())

    technical_verdict = getWeightedVerdictFromScore(technical_score)
    market_verdict = getWeightedVerdictFromScore(market_score)
    economic_verdict = getWeightedVerdictFromScore(economic_score)

    verdict_df = pd.DataFrame(columns=['Indicator', 'Verdict', 'Score'])
    verdict_df = pd.concat([pd.DataFrame([['Technical', changeScoreToVerdict(technical_verdict), technical_verdict]], columns=verdict_df.columns), verdict_df])
    verdict_df = pd.concat([pd.DataFrame([['Market', changeScoreToVerdict(market_verdict), market_verdict]], columns=verdict_df.columns), verdict_df])
    verdict_df = pd.concat([pd.DataFrame([['Economic', changeScoreToVerdict(economic_verdict), economic_verdict]], columns=verdict_df.columns), verdict_df])

    total_score = technical_verdict * weights['Technical'] + market_verdict * weights['Market'] + economic_verdict * weights['Economic']

    verdict_df = pd.concat([pd.DataFrame([['Final', changeScoreToVerdict(total_score), total_score]], columns=verdict_df.columns), verdict_df])
    verdict_df.set_index('Indicator')
    return verdict_df
