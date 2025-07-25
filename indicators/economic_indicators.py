import pandas as pd
from api import inflation, interest_rate, unemployment, gdp_growth, ppp

# Function to calculate Inflation-Adjusted Returns


class EconomicIndicators():

    def __init__(self, df):
        self.df = df

    def calculate_inflation_adjusted_returns(self, df, price_col='Close', inflation_rate_col='inflation_rate'):
        """
        Inflation-Adjusted Returns = (1 + Price Return) / (1 + Inflation Rate) - 1
        """
        df['price_return'] = df[price_col].pct_change()
        df['inflation_adjusted_return'] = (1 + df['price_return']) / (1 + df[inflation_rate_col]) - 1
        return df

    # Function to calculate Real Interest Rate
    def calculate_real_interest_rate(self, df, nominal_interest_rate_col='nominal_interest_rate', inflation_rate_col='inflation_rate'):
        """
        Real Interest Rate = Nominal Interest Rate - Inflation Rate
        """
        df['real_interest_rate'] = df[nominal_interest_rate_col] - df[inflation_rate_col]
        return df

    # Function to calculate GDP Growth Rate
    def calculate_gdp_growth_rate(self, df, gdp_col='gdp_growth_rate'):
        """
        GDP Growth Rate = (GDP_t - GDP_{t-1}) / GDP_{t-1}
        """
        df['gdp_growth_rate'] = df[gdp_col].pct_change(fill_method=None)
        return df

    # Function to calculate Unemployment Rate Impact
    def calculate_unemployment_rate_impact(self, df, unemployment_rate_col='unemployment_rate'):
        """
        Unemployment Rate Impact = Change in Unemployment Rate
        """
        df['unemployment_rate_impact'] = df[unemployment_rate_col].diff()
        return df

    # Function to calculate Purchasing Power Parity (PPP) Adjustment
    def calculate_ppp_adjustment(self, df, price_col='Close', ppp_col='ppp'):
        """
        PPP Adjustment = Price / PPP
        """
        df['ppp_adjusted_price'] = df[price_col] / df[ppp_col]
        return df

    # Global function to calculate all economic indicators

    def calculate_economic_indicators(self):

        inflation_df = inflation.fetch_inflation_rate()
        gdp_df = gdp_growth.fetch_gdp_growth_rate()
        unemployment_df = unemployment.fetch_unemployment_rate()
        interest_rate_df = interest_rate.fetch_interest_rate()
        nominal_interest_rate_df = interest_rate.fetch_nominal_interest_rate()
        ppp_df = ppp.fetch_ppp_data()

        # Merge all DataFrames on 'date'
        df = pd.merge(inflation_df, gdp_df, on='date', how='outer')
        df = pd.merge(df, unemployment_df, on='date', how='outer')
        df = pd.merge(df, interest_rate_df, on='date', how='outer')
        df = pd.merge(df, nominal_interest_rate_df, on='date', how='outer')
        df = pd.merge(df, ppp_df, on='date', how='outer')

        df = df.rename(columns={'date': 'Date'})

        df = pd.merge(df, self.df, on='Date', how='outer')

        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        df.index = pd.to_datetime(df['Date'])
        df.drop(columns=['Date'], inplace=True)

        df[['inflation_rate', 'unemployment_rate', 'nominal_interest_rate', 'interest_rate', 'ppp']] = df[['inflation_rate', 'unemployment_rate', 'nominal_interest_rate', 'interest_rate', 'ppp']].ffill()

        df[df.columns] = df[df.columns].apply(pd.to_numeric, errors='coerce')

        # Calculate Inflation-Adjusted Returns
        df = self.calculate_inflation_adjusted_returns(df)

        # Calculate Real Interest Rate
        df = self.calculate_real_interest_rate(df)

        # Calculate GDP Growth Rate
        df = self.calculate_gdp_growth_rate(df)

        # Calculate Unemployment Rate Impact
        df = self.calculate_unemployment_rate_impact(df)

        # Calculate PPP Adjustment
        df = self.calculate_ppp_adjustment(df)

        return df
