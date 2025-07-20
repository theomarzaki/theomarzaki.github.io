import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import joblib


DATE = '2015-01-01'

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
merged_indicators.to_csv('data/merged_indicators.csv')
merged_indicators.drop(columns=['Date'], inplace=True)

merged_indicators['gdp_growth_rate'] = merged_indicators['gdp_growth_rate'].fillna(0)

x_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()

y_scaler.fit_transform(merged_indicators.Close.values.reshape(-1, 1))

merged_indicators = pd.DataFrame(x_scaler.fit_transform(merged_indicators), columns=merged_indicators.columns)

merged_indicators.iloc[-int(len(merged_indicators) * 0.2):].to_csv('data/testing.csv')
merged_indicators.iloc[:int(len(merged_indicators) * 0.9)].to_csv('data/training.csv')


joblib.dump(x_scaler, 'artifacts/x_scaler.save')
joblib.dump(y_scaler, 'artifacts/y_scaler.save')
