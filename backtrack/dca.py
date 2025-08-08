from backtesting import Strategy
import torch
import numpy as np
import joblib

class DCAStrategy(Strategy):

    def init(self):
        self.WINDOW = 7
        self.INPUT_DIM = 39
        self.initial_cash = 10000

    def next(self):

        size = min(0.1, 0.1 * (self.equity / self.initial_cash))
        self.buy(size=size)

