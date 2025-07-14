import requests
import pandas as pd
import json
from datetime import datetime, timedelta


payload = {}
headers = {
    'Accept': 'application/json'
}


def GetSpread(ticker):
    ticker = "XBTUSD"
    url = F"https://api.kraken.com/0/public/Spread?pair={ticker}"
    unparsed_spreads = requests.request("GET", url, headers=headers, data=payload)
    parsed_spreads = parseSpread(unparsed_spreads.text)
    spread_dataframe = createSpreadDataFrame(parsed_spreads)
    return spread_dataframe


def parseSpread(unparsed_spreads):
    jsonified_response = json.loads(unparsed_spreads)
    if jsonified_response["error"] != []:
        print("FATAL ERROR")

    jsonified_response = jsonified_response["result"]
    ticker_key = list(jsonified_response.keys())[0]
    ticker_response = jsonified_response[ticker_key]
    return ticker_response


def createSpreadDataFrame(parsed_spreads):
    df = pd.DataFrame.from_dict(parsed_spreads)
    spread_dataframe = df.rename({0: 'timestamp', 1: 'bid', 2: 'ask'}, axis=1)

    current_time = datetime.utcnow()
    start_of_previous_day = (current_time - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    spread_dataframe['timestamp'] = start_of_previous_day

    spread_dataframe.set_index('timestamp', inplace=True)

    return spread_dataframe
