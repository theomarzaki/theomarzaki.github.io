import streamlit as st
from ui.sidebar import render_sidebar
from ui.dashboard_html import verdict_card, render_indicator_table
import pandas as pd
from datetime import datetime, timedelta
from processing.technical_indicators import rsi_comment, ma_comment, macd_comment
from processing.market_indicators import vwap_comment, obv_comment, bid_ask_comment

render_sidebar()
st.set_page_config(layout="wide")


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
selected_date = st.selectbox("Choose a date:", options=valid_dates[::-1])
st.markdown("**Only affects technical and market indicators.*")
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
    "Inflation Adjusted Return (US)": (norm_snapshot["inflation_adjusted_return"], "PlaceHolder"),
    "Real Interest Rate (US)": (norm_snapshot["real_interest_rate"], "PlaceHolder"),
    "Unemployment Rate Impact (US)": (norm_snapshot["unemployment_rate_impact"], "PlaceHolder"),
    "PPP Adjustment (US)": (norm_snapshot["ppp_adjusted_price"], "PlaceHolder"),
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
