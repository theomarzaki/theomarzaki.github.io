import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np

DATE = '2015-01-01'


def manipulate_data():

    technical_indicators_data = pd.read_csv('data/technical_indicators.csv')
    market_indicators_data = pd.read_csv('data/market_indicators.csv', index_col=0)
    economic_indicators_data = pd.read_csv('data/economic_indicators.csv')

    if technical_indicators_data.empty or market_indicators_data.empty or economic_indicators_data.empty:
        print(F"Empty DF: {technical_indicators_data.empty}, {market_indicators_data.empty}, {economic_indicators_data.empty}")
        exit()

    technical_indicators_data = technical_indicators_data[(technical_indicators_data['Date'] > DATE)]
    market_indicators_data = market_indicators_data[(market_indicators_data['Date'] > DATE)]
    economic_indicators_data = economic_indicators_data[(economic_indicators_data['Date'] > DATE)]

    merged_indicators = pd.merge(technical_indicators_data, market_indicators_data, how='outer', left_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], right_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume']).merge(economic_indicators_data, how='outer', left_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], right_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    merged_indicators.to_csv('data/merged_indicators.csv')

    merged_indicators = merged_indicators.ffill()

    merged_indicators.drop(columns=['Date'], inplace=True)

    if technical_indicators_data.isna().any().any() or market_indicators_data.isna().any().any() or economic_indicators_data.isna().any().any():
        print(technical_indicators_data[technical_indicators_data.isna().any(axis=1)])
        print(market_indicators_data[market_indicators_data.isna().any(axis=1)])
        print(economic_indicators_data[economic_indicators_data.isna().any(axis=1)])
        exit()

    x_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()

    y_scaler.fit_transform(merged_indicators.Close.values.reshape(-1, 1))

    scaled_data = x_scaler.fit_transform(merged_indicators.values)

    if np.isnan(scaled_data).any():
        print("NaNs detected after scaling.")
        exit()

    merged_indicators = pd.DataFrame(scaled_data, columns=merged_indicators.columns)

    merged_indicators.iloc[-int(len(merged_indicators) * 0.2):].to_csv('data/testing.csv')
    merged_indicators.iloc[:int(len(merged_indicators) * 0.9)].to_csv('data/training.csv')

    joblib.dump(x_scaler, 'artifacts/x_scaler.save')
    joblib.dump(y_scaler, 'artifacts/y_scaler.save')
