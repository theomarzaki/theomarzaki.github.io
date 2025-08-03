import streamlit as st
from ui.sidebar import render_sidebar
import json

render_sidebar()

st.set_page_config(layout="wide")

st.title("Trading Agent")

summary_path = "backtrack/summary/stats_lstm.json"
with open(summary_path, "r") as f:
    stats = json.load(f)

# Metric cards in grid
cols = st.columns(3)
cards = [
    ("Initial Cash", stats["Initial Cash"]),
    ("Final Equity", stats["Final Equity"]),
    ("PnL", stats["PnL"]),
    ("Return (%)", stats["Return (%)"]),
    ("Sharpe Ratio", stats["Sharpe Ratio"]),
    ("Max Drawdown (%)", stats["Max Drawdown (%)"]),
    ("Win Rate (%)", stats["Win Rate (%)"]),
    ("Total Trades", stats["Total Trades"]),
]

for i, (label, value) in enumerate(cards):
    with cols[i % 3]:
        st.metric(label, f"{value:,.2f}" if isinstance(value, float) else str(value))

st.divider()

html_path = "backtrack/plots/backtest_lstm.html"
with open(html_path, "r") as f:
    html = f.read()
st.subheader("Equity Curve")
st.components.v1.html(html, height=800, scrolling=False)
