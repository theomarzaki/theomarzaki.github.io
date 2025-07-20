import streamlit as st
import pandas as pd
import plotly.graph_objects as go


@st.cache_data
def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    return df


# Sidebar - Indicator toggles
st.sidebar.title("BTC Indicators")
show_rsi = st.sidebar.checkbox("RSI (14)", value=True)
show_macd = st.sidebar.checkbox("MACD", value=True)
show_sma = st.sidebar.checkbox("SMA (20)", value=True)
show_ema = st.sidebar.checkbox("EMA (20)", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Toggle indicators to show on chart.")

# Load and process data
df = load_data()

# Main plot
st.title("BTC Price Dashboard")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="BTC Close", line=dict(color="black")))

if show_sma:
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20", line=dict(color="blue", dash="dot")))

if show_ema:
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_20"], name="EMA 20", line=dict(color="orange", dash="dash")))

# Plotly settings
fig.update_layout(
    title="BTC Close Price with Indicators",
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    height=500,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show RSI and MACD in separate subplots
if show_rsi or show_macd:
    st.subheader("Technical Indicator Details")

    if show_rsi:
        st.line_chart(df["RSI"], height=200)

    if show_macd:
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD"))
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD_signal"], name="Signal", line=dict(dash="dot")))
        fig_macd.update_layout(height=300, title="MACD")
        st.plotly_chart(fig_macd, use_container_width=True)
