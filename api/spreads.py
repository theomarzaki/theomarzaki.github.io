import requests
import pandas as pd
import json


payload = {}
headers = {
    'Accept': 'application/json'
}


def GetSpread(ticker):
    ticker = "XBTUSD"
    url = f"https://api.kraken.com/0/public/Spread?pair={ticker}"
    response = requests.get(url)
    data = response.json()
    spread_entries = data['result']["XXBTZUSD"]

    df = pd.DataFrame(spread_entries, columns=["timestamp", "bid", "ask"])

    df['Date'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%Y-%m-%d')

    df = df[['Date', 'bid', 'ask']]
    return df
