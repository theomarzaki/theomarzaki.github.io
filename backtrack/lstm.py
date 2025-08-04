from backtesting import Strategy
import torch
import numpy as np
import joblib
from price_prediction.networks.lstm import LSTMRegressor
from decision.score_based.verdict import GiveVerdictBackTest


class LSTMStrategy(Strategy):

    def init(self):
        self.WINDOW = 7
        self.INPUT_DIM = 39
        self.initial_cash = 10000

        self.lstm_model = LSTMRegressor(input_dim=self.INPUT_DIM)
        self.lstm_model.load_state_dict(torch.load('artifacts/model.save'))
        self.lstm_model.eval()

        self.y_scaler = joblib.load('artifacts/y_scaler.save')
        self.x_scaler = joblib.load('artifacts/x_scaler.save')

    def get_trader_window(self):
        visible_df = self.data.df.iloc[:len(self.data)]
        return visible_df.iloc[-self.WINDOW:]

    def predict_next(self):
        last_n = self.get_trader_window()
        scaled = self.x_scaler.transform(last_n.values)
        input_seq = torch.tensor(scaled, dtype=torch.float32).unsqueeze(0)
        pred_scaled = self.lstm_model(input_seq).squeeze().item()
        pred = self.y_scaler.inverse_transform([[pred_scaled]])
        return pred[0][0]

    def next(self):

        if len(self.data) < self.WINDOW:
            return

        predicted_price = self.predict_next()

        df = self.get_trader_window().copy()
        df.iloc[-1].Close = predicted_price

        decision = GiveVerdictBackTest(df)

        if decision == "Buy":
            size = min(0.1, 0.1 * (self.equity / self.initial_cash))
            self.buy(size=size)

        elif decision == "Sell" and self.position:
            size = min(0.1, 0.1 * (self.equity / self.initial_cash))
            self.sell(size=size)
