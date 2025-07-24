import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ui.sidebar import render_sidebar

render_sidebar()

st.set_page_config(layout="wide")


def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
    df = df.drop_duplicates(subset=['Date'])
    df.set_index("Date", inplace=True)
    return df


subpage = st.sidebar.multiselect("Indicator Settings: ", ["RSI (14)", "MACD", "SMA (20)", "EMA (20)"])

# Load and process data
df = load_data()

# Main plot
st.title("BTC Price Dashboard (~30 Days) - Refreshes Daily")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line=dict(color="black")))

if "SMA (20)" in subpage:
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20", line=dict(color="blue", dash="dot")))

if "EMA (20)" in subpage:
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_20"], name="EMA 20", line=dict(color="orange", dash="dash")))

# Plotly settings
fig.update_layout(
    title="BTC Close Price with Indicators",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    height=500,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show RSI and MACD in separate subplots
if "RSI (14)" in subpage or "MACD" in subpage:
    st.subheader("Technical Indicator Details")

    if "RSI (14)" in subpage:
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df.index, y=df["RSI_14"], name="RSI"))
        fig_rsi.update_layout(height=300, title="RSI")
        st.plotly_chart(fig_rsi, use_container_width=True)

    if "MACD" in subpage:
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD_12_26"], name="MACD"))
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD_sign_12_26"], name="Signal", line=dict(dash="dot")))
        fig_macd.update_layout(height=300, title="MACD")
        st.plotly_chart(fig_macd, use_container_width=True)
