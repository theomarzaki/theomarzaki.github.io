import streamlit as st
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


plt.rcParams.update({"font.size": 10})
plt.rcParams.update({"figure.figsize": (16, 9)})
plt.rcParams["figure.constrained_layout.use"] = True
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.7
plt.rcParams["grid.color"] = "#cccccc"

plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#cb8c86",
           "#60b9ba",
           "#b193c2",
           "#70a582",
           "#d9406d",
           "#a79f6d"])


sns.set_context(
    "paper", font_scale=3, rc={"lines.linewidth": 3.5, "figure.figsize": (16, 9)}
)


current_time = datetime.utcnow()
start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')


technical_indicators = pd.read_csv('plotting/technical_indicators.csv')

technical_indicators = technical_indicators[(technical_indicators['Date'] > start_of_week_previous) & (technical_indicators['Date'] <= start_of_week_ahead)]

st.title("BTC Techanical Indicator (~30 Days) - Refreshes Daily")

fig = plt.figure(figsize=(16, 9))
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['Close'], label='Close')
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['High'], label='High')
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['SMA_20'], label='SMA')
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['EMA_20'], label='EMA')
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['hband'], label='High BB')
sns.lineplot(x=technical_indicators['Date'], y=technical_indicators['lband'], label='Low BB')

plt.xticks(rotation=90)
plt.xlabel('Date')
plt.ylabel('USD ($)')
st.pyplot(fig)
