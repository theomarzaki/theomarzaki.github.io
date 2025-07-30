import numpy as np


def calculate_scores(df):
    """
    Calculate scores for each market indicator and aggregate them into a final decision.
    """
    # Initialize scores
    df['Score'] = 0

    # Bid-Ask Spread
    df['Score'] += np.where(df['bid_ask_spread'] < 0.1, 1,
                            np.where(df['bid_ask_spread'] > 0.5, -1, 0))

    # Order Book Depth
    df['Score'] += np.where(df['order_book_depth'] > 1000, 1,
                            np.where(df['order_book_depth'] < 500, -1, 0))

    # Cumulative Price Volume
    df['cumulative_price_volume_trend'] = df['cumulative_price_volume'].diff().apply(lambda x: 1 if x > 0 else -1)
    df['Score'] += df['cumulative_price_volume_trend']

    # Cumulative Volume
    df['cumulative_volume_trend'] = df['cumulative_volume'].diff().apply(lambda x: 1 if x > 0 else -1)
    df['Score'] += df['cumulative_volume_trend']

    # VWAP
    df['Score'] += np.where(df['Close'] > df['vwap'], 1, -1)

    return df

# Step 2: Make Decisions Based on Scores


def make_decisions(df):
    """
    Make buy/hold/sell decisions based on the aggregated score.
    """

    calculate_scores(df)

    df['Decision'] = np.where(df['Score'] >= 1, 'Buy',
                              np.where(df['Score'] <= -1, 'Sell', 'Hold'))
    return df
