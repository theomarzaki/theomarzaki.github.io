import torch
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta


def predict(model):

    WINDOW_SIZE = 7

    data = pd.read_csv('data/merged_indicators.csv', index_col=0)

    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=WINDOW_SIZE)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    data = data[(data['Date'] > start_of_week_previous)]
    data = data.drop_duplicates(subset=['Date'])
    data.drop(columns=['Date'], inplace=True)

    model.load_state_dict(torch.load('artifacts/model.save'))

    y_scaler = joblib.load('artifacts/y_scaler.save')
    x_scaler = joblib.load('artifacts/x_scaler.save')

    model.eval()
    predictions = []
    input_seq = data.copy()

    input_seq = x_scaler.transform(input_seq.values)

    for _ in range(WINDOW_SIZE):
        input_tensor = torch.tensor(input_seq, dtype=torch.float32).unsqueeze(0)  # shape: (1, 7, features)
        with torch.no_grad():
            next_pred = model(input_tensor).squeeze().item()

        predictions.append(next_pred)

        # Append predicted close to input sequence for next step
        next_features = input_seq[-1].copy()
        next_features[0] = next_pred  # replace close price
        input_seq = np.vstack([input_seq[1:], next_features])  # slide window forward

    predictions = y_scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    pd.DataFrame(predictions).to_csv('price_prediction/results/price_predictions.csv')
