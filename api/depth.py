import pandas as pd
import requests
from datetime import datetime, timedelta


def fetch_kraken_order_book(ticker='XBTUSD', depth=1):
    url = 'https://api.kraken.com/0/public/Depth'
    params = {
        'pair': ticker,
        'count': depth
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from Kraken API: {response.status_code}")


def GetOrderBook(kraken_ticker):
    order_book = fetch_kraken_order_book(kraken_ticker)
    kraken_ticker = list(order_book['result'].keys())[0]
    asks = order_book['result'][kraken_ticker]['asks']
    bids = order_book['result'][kraken_ticker]['bids']

    # Get the current timestamp and convert it to the start of the day
    current_time = datetime.utcnow()
    start_of_previous_day = (current_time - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Create a DataFrame with ask and bid volumes, using the start of the day as the timestamp
    kraken_data = pd.DataFrame({
        'timestamp': [start_of_previous_day],
        'ask_volume': [float(asks[0][1])],
        'bid_volume': [float(bids[0][1])]
    })

    # Set the timestamp as the index
    kraken_data.set_index('timestamp', inplace=True)
    return kraken_data
