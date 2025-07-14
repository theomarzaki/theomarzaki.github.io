import streamlit as st
import pandas as pd
import numpy as np


# Load data
# preds = pd.read_csv("data/predictions.csv")
# prices = pd.read_csv("data/raw_data.csv")

st.title("Bitcoin Price Prediction vs Actual")

# fig, ax = plt.subplots()
# ax.plot(prices['date'], prices['price'], label='Actual')
# ax.plot(preds['date'], preds['prediction'], label='Predicted')
# ax.legend()
# st.pyplot(fig)

st.subheader("PnL & Metrics")
