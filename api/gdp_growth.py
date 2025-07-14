import requests
import pandas as pd
from api import FRED_API_KEY, OBSERVATION_START, OBSERVATION_END


def fetch_gdp_growth_rate():
    """
    Fetch the latest GDP growth rate from FRED.
    """
    url = f'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'A191RL1Q225SBEA',  # Real GDP Growth Rate
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
    df['gdp_growth_rate'] = pd.to_numeric(df['value'])
    return df[['date', 'gdp_growth_rate']].dropna()
