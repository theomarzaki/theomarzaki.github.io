import streamlit as st
from ui.sidebar import render_sidebar
from ui.dashboard_html import verdict_card, render_indicator_table, render_final_table
import pandas as pd
from datetime import datetime, timedelta
from processing.technical_indicators import rsi_comment, ma_comment, macd_comment
from processing.market_indicators import vwap_comment, obv_comment, bid_ask_comment
from processing.macro_indicators import get_real_interest_rate_comment, get_inflation_adjusted_return_comment, get_ppp_adjustment_comment, get_unemployment_rate_impact_comment
import json


render_sidebar()
st.set_page_config(layout="wide")


with open("backtrack/summary/stats_lstm.json", "r") as f:
    stats = json.load(f)


def colorize(value):
    return "#d4f4dd" if value > 0 else "#f8d7da"  # green or red background


col1, col2 = st.columns(2)

with col1:
    pnl_bg = colorize(stats["PnL"])
    st.markdown(f"""
        <div style='
            background-color: {pnl_bg};
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        '>
            <h3 style='margin-bottom: 0.5rem;'>PnL</h3>
            <span style='font-size: 3rem; font-weight: 800;'>{stats["PnL"]:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    ret_bg = colorize(stats["Return (%)"])
    st.markdown(f"""
        <div style='
            background-color: {ret_bg};
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        '>
            <h3 style='margin-bottom: 0.5rem;'>Return (%)</h3>
            <span style='font-size: 3rem; font-weight: 800;'>{stats["Return (%)"]:,.2f}%</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("See more metrics at Asset Trader page")

st.divider()


def signal_label(signal):
    if signal == "Buy":
        return "green"
    elif signal == "Sell":
        return "red"
    else:
        return "grey"


def load_data():
    data = pd.read_csv('data/verdict.csv')
    return data


df = load_data()
data = pd.read_csv('data/merged_indicators.csv')

current_time = datetime.utcnow()
start_of_week_ahead = (current_time - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
# Filter to just those dates
data = data.drop_duplicates(subset=['Date'])
data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
data["OBV_diff"] = data["OBV"].diff()
valid_dates = data.loc[(data.Date >= start_of_week_ahead)].Date

# Assets section
# st.sidebar.subheader("Configurations: ")

selected_date = st.sidebar.selectbox("Choose a date:", options=valid_dates[::-1])
st.sidebar.markdown("**Only affects technical and market indicators.*")
snapshot = data[data['Date'] == selected_date].iloc[-1]
if snapshot.empty:
    st.error(f"No data for selected date: {selected_date}")
norm_snapshot = data[data['Date'] == current_time.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
                     ].iloc[0]

technical_indicators = {
    "RSI": (snapshot['RSI_14'], rsi_comment(snapshot['RSI_14'])),
    "SMA": (snapshot['SMA_20'], ma_comment(snapshot['Close'], snapshot['SMA_20'], snapshot['EMA_20'])),
    "EMA": (snapshot['EMA_20'], ma_comment(snapshot['Close'], snapshot['SMA_20'], snapshot['EMA_20'])),
    "MACD": (snapshot['MACD_12_26'], macd_comment(snapshot['MACD_12_26'])),
}

market_indicators = {
    "OBV Diff": (snapshot['OBV_diff'], obv_comment(snapshot['OBV_diff'])),
    "VWAP": (round(snapshot["vwap"], 2), vwap_comment(snapshot["Close"], norm_snapshot["vwap"])),
    "BID ASK SPREAD": (round(snapshot["bid_ask_spread"], 2), bid_ask_comment(snapshot["bid_ask_spread"])),
}

macro_indicators = {
    "Inflation Adjusted Return (US)": (
        round(norm_snapshot["inflation_adjusted_return"], 2),
        get_inflation_adjusted_return_comment(norm_snapshot["inflation_adjusted_return"])
    ),
    "Real Interest Rate (US)": (
        round(norm_snapshot["real_interest_rate"], 2),
        get_real_interest_rate_comment(norm_snapshot["real_interest_rate"])
    ),
    "Unemployment Rate Impact (US)": (
        round(norm_snapshot["unemployment_rate_impact"], 2),
        get_unemployment_rate_impact_comment(norm_snapshot["unemployment_rate_impact"])
    ),
    "PPP Adjustment (US)": (
        round(norm_snapshot["ppp_adjusted_price"], 2),
        get_ppp_adjustment_comment(norm_snapshot["ppp_adjusted_price"])
    ),
}

tech_label = df[(df['Indicator'] == "Technical")].Verdict.values[0]
market_label = df[(df['Indicator'] == "Market")].Verdict.values[0]
macro_label = df[(df['Indicator'] == "Economic")].Verdict.values[0]
total_label = df[(df['Indicator'] == "Final")].Verdict.values[0]

# Map scores to labels/colors
tech_color = signal_label(tech_label)
market_color = signal_label(market_label)
macro_color = signal_label(macro_label)
total_color = signal_label(total_label)


st.title("BTC Market Suggested Actions Based on Signals & Price Predictions")
# --- Technical ---
st.markdown(verdict_card("Technical", tech_label, tech_color), unsafe_allow_html=True)
with st.expander("See technical indicators"):
    st.markdown(render_indicator_table(technical_indicators), unsafe_allow_html=True)

# # --- Market ---
st.markdown(verdict_card("Market", market_label, market_color), unsafe_allow_html=True)
with st.expander("See market indicators"):
    st.markdown(render_indicator_table(market_indicators), unsafe_allow_html=True)

# # --- Macro ---
st.markdown(verdict_card("Macro", macro_label, macro_color), unsafe_allow_html=True)
with st.expander("See macro indicators"):
    st.markdown(render_indicator_table(macro_indicators), unsafe_allow_html=True)

final_indicators = {
    "Technical": ("33%", tech_label),
    "Market": ("33%", market_label),
    "Macro": ("33%", macro_label),
}


total_score = 0.99
# --- Final ---
st.markdown(verdict_card("Final Suggestion", total_label, total_color), unsafe_allow_html=True)
with st.expander("Final score breakdown"):
    st.markdown(render_final_table(final_indicators), unsafe_allow_html=True)
