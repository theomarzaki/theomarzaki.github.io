import requests
import pandas as pd


def fetch_ppp_data(country_code='US'):
    """
    Fetch Purchasing Power Parity (PPP) data for a specific country.
    """
    url = f'https://api.worldbank.org/v2/country/{country_code}/indicator/PA.NUS.PPP?format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ppp_data = data[1]  # The actual data is in the second element of the JSON response
        ppp_df = pd.DataFrame(ppp_data)
        ppp_df = ppp_df[['date', 'value']].rename(columns={'value': 'ppp'})
        ppp_df['date'] = pd.to_datetime(ppp_df['date'])

        return ppp_df
    else:
        print(f"Failed to fetch PPP data. Status code: {response.status_code}")
        return None
