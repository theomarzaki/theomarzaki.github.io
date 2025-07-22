import streamlit as st
from ui.sidebar import render_sidebar
import pandas as pd

render_sidebar()
st.set_page_config(layout="wide")


def signal_label(signal):
    if signal == "Buy":
        return "green"
    elif signal == "Sell":
        return "red"
    else:
        return "grey"


def verdict_card(title, label, bg_color):
    return f"""
    <div style="
        background-color: {bg_color};
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 1rem; margin-bottom: 0.5rem;">{title}</div>
        {label}
    </div>
    """


def load_data():
    data = pd.read_csv('data/verdict.csv')
    return data


technical_indicators = {
    "RSI": (34, "Oversold", "↑"),
    "MACD": (-1.2, "Bearish", "↓"),
    "MA Crossover": ("No", "Neutral", "→")
}

market_indicators = {
    "Funding Rate": (0.015, "Neutral", "→"),
    "Open Interest": ("Increasing", "Bullish", "↑")
}

macro_indicators = {
    "CPI YoY": (3.2, "High Inflation", "↓"),
    "DXY": (104.5, "Strong Dollar", "↓")
}


df = load_data()

tech_label = df[(df['Indicator'] == "Technical")].Verdict.values[0]
market_label = df[(df['Indicator'] == "Market")].Verdict.values[0]
macro_label = df[(df['Indicator'] == "Economic")].Verdict.values[0]
total_label = df[(df['Indicator'] == "Final")].Verdict.values[0]

# Map scores to labels/colors
tech_color = signal_label(tech_label)
market_color = signal_label(market_label)
macro_color = signal_label(macro_label)
total_color = signal_label(total_label)


# Table formatter
def render_indicator_table(indicators):
    rows = ""
    for name, (value, comment, arrow) in indicators.items():
        rows += f"<tr><td>{name}</td><td>{value}</td><td>{comment}</td><td>{arrow}</td></tr>"
    return f"""
    <table style='width:100%; text-align:left; font-size: 0.9rem; border-spacing: 0 4px;'>
        <tr><th>Indicator</th><th>Value</th><th>Comment</th><th>↕</th></tr>
        {rows}
    </table>
    """


st.title("BTC Market Suggested Actions Based on Signals & Price Predictions")
# --- Technical ---
st.markdown(verdict_card("Technical", tech_label, tech_color), unsafe_allow_html=True)
with st.expander("See technical indicators"):
    st.markdown(render_indicator_table(technical_indicators), unsafe_allow_html=True)

# --- Market ---
st.markdown(verdict_card("Market", market_label, market_color), unsafe_allow_html=True)
with st.expander("See market indicators"):
    st.markdown(render_indicator_table(market_indicators), unsafe_allow_html=True)

# --- Macro ---
st.markdown(verdict_card("Macro", macro_label, macro_color), unsafe_allow_html=True)
with st.expander("See macro indicators"):
    st.markdown(render_indicator_table(macro_indicators), unsafe_allow_html=True)

total_score = 0.99
# --- Final ---
st.markdown(verdict_card("Final Suggestion", total_label, total_color), unsafe_allow_html=True)
with st.expander("Breakdown of total score"):
    st.markdown(f"""
    - **Technical** (33%): {tech_label}
    - **Market** (33%): {market_label}
    - **Macro** (33%): {macro_label}

    **Combined Score:** {total_score:.2f} → **{total_label}**
    """)
