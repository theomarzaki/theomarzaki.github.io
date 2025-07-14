import requests
import re
import pandas as pd
import yfinance as yf


def get_top_5_cryptos():
    asset_url = "https://api.kraken.com/0/public/AssetPairs"
    asset_response = requests.get(asset_url).json()

    # Extract USD trading pairs
    usd_pairs = {pair: details for pair, details in asset_response['result'].items() if re.search(r"USD$", pair)}

    # Step 2: Fetch volume data from Kraken's Ticker endpoint
    ticker_url = "https://api.kraken.com/0/public/Ticker"
    pair_list = ",".join(usd_pairs.keys())  # Format for API request
    ticker_response = requests.get(ticker_url, params={"pair": pair_list}).json()

    # Extract volume data (24h rolling volume is in ['v'][1])
    volumes = {pair: float(details['v'][1]) for pair, details in ticker_response['result'].items()}

    # Step 3: Get the top 5 cryptos by volume
    top_5_pairs = sorted(volumes.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_symbols = [usd_pairs[pair]['base'] for pair, _ in top_5_pairs]  # Kraken base symbol

    print(top_5_symbols)

    # # Sort by trading volume (descending) and get the top 5
    # top_5 = sorted(cryptos, key=lambda x: x[2], reverse=True)[:5]
    # symbols = [crypto[1] for crypto in top_5]  # Kraken symbols
    return top_5_symbols


def get_popular_tickers_kraken(limit=5):
    # Step 1: Fetch all asset pairs from Kraken
    asset_url = "https://api.kraken.com/0/public/AssetPairs"
    asset_response = requests.get(asset_url).json()

    if asset_response.get("error"):
        raise Exception(f"Kraken API Error: {asset_response['error']}")

    asset_pairs = asset_response["result"].keys()  # Get all trading pairs

    # Step 2: Fetch ticker info to get 24h volume
    ticker_url = "https://api.kraken.com/0/public/Ticker"
    ticker_response = requests.get(ticker_url, params={"pair": ",".join(asset_pairs)}).json()

    if ticker_response.get("error"):
        raise Exception(f"Kraken API Error: {ticker_response['error']}")

    # Step 3: Extract volume data
    volumes = {
        pair: float(details['v'][1])  # 'v' key: [rolling volume, last 24h volume]
        for pair, details in ticker_response["result"].items()
    }

    # Step 4: Sort tickers by 24h volume (descending order)
    top_tickers = sorted(volumes.items(), key=lambda x: x[1], reverse=True)[:limit]

    return top_tickers


def get_popular_assets_by_market_position(limit=5):
    # Step 1: Fetch all trading pairs from Kraken
    asset_url = "https://api.kraken.com/0/public/AssetPairs"
    asset_response = requests.get(asset_url).json()

    if asset_response.get("error"):
        raise Exception(f"Kraken API Error: {asset_response['error']}")

    # Extract unique base assets from USD trading pairs
    assets = set()
    for pair, details in asset_response["result"].items():
        if re.search(r"USD$", pair):  # Ensure we're looking at USD pairs
            assets.add(details["base"])

    # Step 2: Convert Kraken asset symbols to Yahoo Finance format (BTC → BTC-USD)
    yf_symbols = [asset + "-USD" for asset in assets]

    # Step 3: Fetch market cap data from Yahoo Finance
    market_caps = {}
    for symbol in yf_symbols:
        data = yf.Ticker(symbol).info
        market_caps[symbol] = data.get("marketCap", 0)  # Default to 0 if missing

    # Step 4: Sort by market cap in descending order
    sorted_assets = sorted(market_caps.items(), key=lambda x: x[1], reverse=True)[:limit]

    # Convert to DataFrame
    df = pd.DataFrame(sorted_assets, columns=["Crypto", "Market Cap"])

    return df
