import numpy as np


def calculate_scores(df):
    """
    Calculate scores for each indicator and aggregate them into a final decision.
    """
    df['Score'] = 0

    # SMA_20
    df['Score'] += np.where(df['Close'] > df['SMA_20'], 1, -1)

    # RSI_14
    df['Score'] += np.where(df['RSI_14'] < 30, 1, np.where(df['RSI_14'] > 70, -1, 0))

    # Bollinger Bands
    df['Score'] += np.where(df['Close'] < df['lband'], 1,
                            np.where(df['Close'] > df['hband'], -1, 0))

    # MACD
    df['Score'] += np.where(df['MACD_12_26'] > df['MACD_sign_12_26'], 1, -1)

    # OBV
    df['OBV_Trend'] = df['OBV'].diff().apply(lambda x: 1 if x > 0 else -1)
    df['Score'] += df['OBV_Trend']

    return df

# Step 2: Make Decisions Based on Scores


def make_decisions(df):
    """
    Make buy/hold/sell decisions based on the aggregated score.
    """

    calculate_scores(df)

    df['Decision'] = np.where(df['Score'] >= 3, 'Buy',
                              np.where(df['Score'] <= -3, 'Sell', 'Hold'))
    return df
