import requests
import pandas as pd
from api import ALPHA_VANTAGE_API_KEY, FRED_API_KEY


def fetch_interest_rate():
    """
    Fetch the latest interest rate from Alpha Vantage.
    """
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'FEDERAL_FUNDS_RATE',
        'apikey': ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df['interest_rate'] = pd.to_numeric(df['value'])
    return df[['date', 'interest_rate']]


def fetch_nominal_interest_rate(series_id='INTDSRUSM193N'):
    """
    Fetch Nominal Interest Rate data from FRED.
    """
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        interest_data = data['observations']
        interest_df = pd.DataFrame(interest_data)
        interest_df = interest_df[['date', 'value']].rename(columns={'value': 'nominal_interest_rate'})
        interest_df['date'] = pd.to_datetime(interest_df['date'])
        return interest_df
    else:
        print(f"Failed to fetch interest rate data. Status code: {response.status_code}")
        return None
