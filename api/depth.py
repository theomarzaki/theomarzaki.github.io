import pandas as pd
import requests
from datetime import datetime


def GetOrderBook(ticker='XBTUSD'):
    url = 'https://api.kraken.com/0/public/Depth'
    params = {'pair': 'XBTUSD', 'count': 10}
    response = requests.get(url, params=params)
    data = response.json()

    depth = data['result']['XXBTZUSD']
    bids = pd.DataFrame(depth['bids'], columns=['price', 'bid_volume', 'timestamp'])
    asks = pd.DataFrame(depth['asks'], columns=['price', 'ask_volume', 'timestamp'])

    bids[['price', 'bid_volume']] = bids[['price', 'bid_volume']].astype(float)
    asks[['price', 'ask_volume']] = asks[['price', 'ask_volume']].astype(float)

    bids = bids.drop(columns='timestamp')
    asks = asks.drop(columns='timestamp')

    merged_depth = pd.concat([bids, asks], axis=1)

    merged_depth['Date'] = datetime.utcnow().strftime('%Y-%m-%d')

    merged_depth = merged_depth[['Date', 'price', 'bid_volume', 'ask_volume']]
    daily_volume = merged_depth.groupby('Date')[['bid_volume', 'ask_volume']].sum().reset_index()

    return daily_volume
