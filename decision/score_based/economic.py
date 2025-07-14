import numpy as np


def calculate_scores(df):
    """
    Calculate scores for each market indicator and aggregate them into a final decision.
    """

    df['Score'] = 0

    # Inflation Rate
    df['Score'] += np.where(df['inflation_rate'] < 0.03, 1, np.where(df['inflation_rate'] > 0.05, -1, 0))

    # GDP Growth Rate
    df['Score'] += np.where(df['gdp_growth_rate'] > 0.02, 1, np.where(df['gdp_growth_rate'] < 0.00, -1, 0))

    # Unemployment Rate
    df['Score'] += np.where(df['unemployment_rate'] < 5.5, 1, np.where(df['unemployment_rate'] > 6.5, -1, 0))

    # Interest Rate
    df['Score'] += np.where(df['interest_rate'] < 3.0, 1, np.where(df['interest_rate'] > 4.0, -1, 0))

    # Nominal Interest Rate
    df['Score'] += np.where(df['nominal_interest_rate'] < 3.5, 1, np.where(df['nominal_interest_rate'] > 4.5, -1, 0))

    # PPP
    df['Score'] += np.where(df['ppp'] > 1.2, 1, np.where(df['ppp'] < 1.0, -1, 0))

    # Price Return
    df['Score'] += np.where(df['price_return'] > 0.03, 1, np.where(df['price_return'] < 0.01, -1, 0))

    # Inflation-Adjusted Return
    df['Score'] += np.where(df['inflation_adjusted_return'] > 0.02, 1, np.where(df['inflation_adjusted_return'] < 0.01, -1, 0))

    # Real Interest Rate
    df['Score'] += np.where(df['real_interest_rate'] > 2.0, 1, np.where(df['real_interest_rate'] < 1.5, -1, 0))

    # Unemployment Rate Impact
    df['Score'] += np.where(df['unemployment_rate_impact'] > -0.3, 1, np.where(df['unemployment_rate_impact'] < -0.5, -1, 0))

    # PPP-Adjusted Price
    df['Score'] += np.where(df['ppp_adjusted_price'] > 32000, 1, np.where(df['ppp_adjusted_price'] < 30000, -1, 0))

    return df

# Step 2: Make Decisions Based on Scores


def make_decisions(df):
    """
    Make buy/hold/sell decisions based on the aggregated score.
    """

    calculate_scores(df)

    df['Decision'] = np.where(df['Score'] >= 2, 'Buy',
                              np.where(df['Score'] <= -2, 'Sell', 'Hold'))
    return df
