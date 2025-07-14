import requests
import pandas as pd
from api import FRED_API_KEY, OBSERVATION_START, OBSERVATION_END


def fetch_inflation_rate():
    """
    Fetch the latest inflation rate (CPI) from FRED.
    """
    url = f'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'CPIAUCSL',  # Consumer Price Index for All Urban Consumers
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': OBSERVATION_START,
        'observation_end': OBSERVATION_END,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'])

    # Calculate inflation rate (YoY % change)
    df['inflation_rate'] = df['value'].pct_change(periods=12) * 100
    return df[['date', 'inflation_rate']].dropna()
