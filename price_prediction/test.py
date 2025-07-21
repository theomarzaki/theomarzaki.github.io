from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import joblib


def test(model):

    WINDOW_SIZE = 7
    BATCH_SIZE = 64
    MODEL_DIM = 64

    testing_data = pd.read_csv('data/testing.csv', index_col=0)
    features_test = []
    labels_test = []

    for i in range(len(testing_data) - WINDOW_SIZE):
        features_test.append(testing_data.iloc[i:i + WINDOW_SIZE])
        labels_test.append(testing_data.iloc[i + WINDOW_SIZE].Close)

    features_test = torch.tensor(np.array(features_test))
    labels_test = torch.tensor(np.array(labels_test))

    dataset_test = TensorDataset(features_test, labels_test)
    test_loader = DataLoader(dataset_test, batch_size=BATCH_SIZE, shuffle=True)

    model.load_state_dict(torch.load('artifacts/model.save'))
    model.eval()

    scaler = joblib.load('artifacts/y_scaler.save')

    all_preds = []
    all_targets = []

    with torch.no_grad():
        for xb, yb in test_loader:
            preds = model(xb.float())
            all_preds.append(preds.numpy())
            all_targets.append(yb.numpy())

    preds = np.concatenate(all_preds).flatten()
    targets = np.concatenate(all_targets).flatten()

    # Inverse scale to get actual BTC prices
    preds_unscaled = scaler.inverse_transform(preds.reshape(-1, 1)).flatten()
    targets_unscaled = scaler.inverse_transform(targets.reshape(-1, 1)).flatten()

    mse = mean_squared_error(targets_unscaled, preds_unscaled)
    mae = mean_absolute_error(targets_unscaled, preds_unscaled)
    r2 = r2_score(targets_unscaled, preds_unscaled)

    results = {
        'MSE': mse,
        'MAE': mae,
        'R2': r2
    }

    print(results)

    pd.DataFrame(results, index=[0]).to_csv('price_prediction/results/testing_results.csv')
