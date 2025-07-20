import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta


@st.cache_data
def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
    df.set_index("Date", inplace=True)
    return df


# Sidebar - Indicator toggles
st.sidebar.title("BTC Indicators")
st.sidebar.markdown("---")
st.sidebar.caption("Toggle indicators to show on chart.")
show_rsi = st.sidebar.checkbox("RSI (14)", value=False)
show_macd = st.sidebar.checkbox("MACD", value=False)
show_sma = st.sidebar.checkbox("SMA (20)", value=False)
show_ema = st.sidebar.checkbox("EMA (20)", value=False)

# Load and process data
df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Price + Indicators", "Future Price Prediction", "Risk Modeling", "Suggested Actions"])

with tab1:
    # Main plot
    st.title("BTC Price Dashboard (~30 Days) - Refreshes Daily")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line=dict(color="black")))

    if show_sma:
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20", line=dict(color="blue", dash="dot")))

    if show_ema:
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
    if show_rsi or show_macd:
        st.subheader("echnical Indicator Details")

        if show_rsi:
            st.line_chart(df["RSI_14"], height=200)

        if show_macd:
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD_12_26"], name="MACD"))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD_sign_12_26"], name="Signal", line=dict(dash="dot")))
            fig_macd.update_layout(height=300, title="MACD")
            st.plotly_chart(fig_macd, use_container_width=True)

with tab2:
    st.subheader("BTC Price Predictions")
    st.info("LSTM/Transformer predictions here.")
    st.caption("e.g., predicted vs actual chart, buy/sell markers, model confidence, etc.")

with tab3:
    st.subheader("Risk Modeling")
    st.info("RISKS.")
    st.caption("RISKS.")

with tab4:
    st.subheader("Actionable Suggestions")
    st.info("BUY OR SELL.")
    st.caption("Different stuff.")

