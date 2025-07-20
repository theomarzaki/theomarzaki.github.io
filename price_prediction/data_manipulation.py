import pandas as pd
import seaborn as sns
from sklearn.preprocessing import RobustScaler
import joblib


DATE = '2020-01-01'

historical_data = pd.read_csv('data/historical_data.csv')
technical_indicators_data = pd.read_csv('data/technical_indicators.csv')
market_indicators_data = pd.read_csv('data/market_indicators.csv')
economic_indicators_data = pd.read_csv('data/economic_indicators.csv')

market_indicators_data = market_indicators_data.rename(columns={'timestamp': 'Date'})

technical_indicators_data = technical_indicators_data[(technical_indicators_data['Date'] > DATE)]
market_indicators_data = market_indicators_data[(market_indicators_data['Date'] > DATE)]
economic_indicators_data = economic_indicators_data[(economic_indicators_data['Date'] > DATE)]

merged_indicators = pd.merge(technical_indicators_data, market_indicators_data, how='outer', left_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], right_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume']).merge(economic_indicators_data, how='outer', left_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], right_on=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
merged_indicators.bfill(inplace=True)
merged_indicators.drop(columns=['Date'], inplace=True)

scaler = RobustScaler()

merged_indicators = pd.DataFrame(scaler.fit_transform(merged_indicators), columns=merged_indicators.columns)

merged_indicators.iloc[-int(len(merged_indicators) * 0.2):].to_csv('data/testing.csv')
merged_indicators.iloc[:int(len(merged_indicators) * 0.8)].to_csv('data/training.csv')

joblib.dump(scaler, 'artifacts/scaler.save')
