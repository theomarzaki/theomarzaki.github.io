from backtesting import Strategy
import torch
import numpy as np
import joblib
from price_prediction.networks.lstm import LSTMRegressor


class LSTMStrategy(Strategy):

    def init(self):
        self.WINDOW = 7
        self.INPUT_DIM = 39

        self.model = LSTMRegressor(input_dim=self.INPUT_DIM)
        self.model.load_state_dict(torch.load('artifacts/model.save'))
        self.model.eval()

        self.y_scaler = joblib.load('artifacts/y_scaler.save')
        self.x_scaler = joblib.load('artifacts/x_scaler.save')

    def predict_next(self):

        print(self.data)
        last_n = self.data[-self.WINDOW:]
        print(last_n)
        scaled = self.x_scaler.transform(last_n.values)
        input_seq = scaled.reshape(1, self.WINDOW, 1)
        pred_scaled = self.model.predict(input_seq)
        pred = self.y_scaler.inverse_transform(pred_scaled)
        return pred[0][0]

    def next(self):

        current_index = len(self.data) - 1  # current step index
        current_date = self.data.df.index[current_index]
        current_price = self.data.Close[-1]

        print(f"{current_date.date()} | Step: {current_index} | Price: {current_price:.2f}")

        if len(self.data) < self.WINDOW:
            return

        predicted_price = self.predict_next()
        current_price = self.data.Close[-1]

        if predicted_price > current_price and not self.position:
            self.buy()
        elif predicted_price < current_price and self.position:
            self.sell()
