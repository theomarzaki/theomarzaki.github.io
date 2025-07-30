import pandas as pd
import requests


def fetchSentiment():

    url = "https://api.alternative.me/fng/?limit=0"  # fetch all available history
    resp = requests.get(url)
    data = resp.json().get("data", [])

    fg_df = pd.DataFrame(data)
    fg_df['Date'] = pd.to_datetime(fg_df['timestamp'].astype(int), unit='s')
    fg_df['Sentiment'] = fg_df['value'].astype(int)
    fg_df = fg_df[['Date', 'Sentiment']]

    return fg_df
