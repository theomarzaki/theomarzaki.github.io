import streamlit as st
from ui.sidebar import render_sidebar
import json

render_sidebar()

st.set_page_config(layout="wide")

st.title("Trading Agent")

summary_path = "backtrack/summary/stats_lstm.json"
with open(summary_path, "r") as f:
    stats = json.load(f)

    def colorize(label, value):
        if label in ["PnL", "Return (%)"]:
            return "green" if value > 0 else "red"
        elif label == "Sharpe Ratio":
            return "green" if value >= 1 else ("orange" if value > 0 else "red")
        elif label == "Max Drawdown (%)":
            return "red" if value > 20 else "orange" if value > 10 else "green"
        elif label == "Win Rate (%)":
            return "green" if value >= 50 else "orange"
        else:
            return "gray"

    # Metric cards
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
    bg_color = colorize(label, value)
    with cols[i % 3]:
        st.markdown(f"""
            <div style='
                background-color: #f9f9f9;
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            '>
                <div style='font-weight: 600; font-size: 1.1rem; margin-bottom: 0.25rem;'>{label}</div>
                <div style='
                    background-color: {bg_color};
                    padding: 0.3rem 0.8rem;
                    border-radius: 12px;
                    font-size: 1.3rem;
                    font-weight: 700;
                    width: fit-content;
                '>{value:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

html_path = "backtrack/plots/backtest_lstm.html"
with open(html_path, "r") as f:
    html = f.read()
st.subheader("quity Curve")
st.components.v1.html(html, height=800, scrolling=False)
