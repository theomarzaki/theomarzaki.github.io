import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load Data

technical_indicators = pd.read_csv('plotting/technical_indicators.csv')

st.title('Technical Indicators for BTC')

fig, ax = plt.subplots()
ax.plot(technical_indicators['Open'], label='Open')
ax.plot(technical_indicators['Close'], label='Close')
ax.plot(technical_indicators['High'], label='High')
ax.plot(technical_indicators['SMA_20'], label='SMA')
ax.plot(technical_indicators['EMA_20'], label='EMA')
ax.plot(technical_indicators['RSI_14'], label='RSI')
ax.plot(technical_indicators['hband'], label='High Band')
ax.plot(technical_indicators['lband'], label='Low Band')
ax.legend()
st.pyplot(fig)


# fig, ax = plt.subplots()
# ax.plot(prices['date'], prices['price'], label='Actual')
# ax.plot(preds['date'], preds['prediction'], label='Predicted')
# ax.legend()
# st.pyplot(fig)

# st.subheader("PnL & Metrics")
