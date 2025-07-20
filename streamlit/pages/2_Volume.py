import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots


@st.cache_data
def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
    return df


# Create dual-axis chart
fig = go.Figure()

df = load_data()

# Price line (left y-axis)
fig.add_trace(go.Scatter(
    x=df["Date"],
    y=df["Close"],
    name="BTC Price",
    line=dict(color="royalblue"),
    yaxis="y1"
))

# Volume bars (right y-axis)
fig.add_trace(go.Bar(
    x=df["Date"],
    y=df["Volume"],
    name="Volume",
    marker_color="lightgray",
    yaxis="y2",
    opacity=0.4
))

# Layout
fig.update_layout(
    title="BTC Price vs Trading Volume",
    xaxis=dict(title="Date"),
    yaxis=dict(
        title="Price (USD)",
        side="left",
        showgrid=False
    ),
    yaxis2=dict(
        title="Volume",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=500
)

st.plotly_chart(fig, use_container_width=True)


fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=["Raw Volume + MA", "Volume Ratio / OBV"])

df["vol_ma_7"] = df["Volume"].rolling(window=7).mean()

# Volume + MA
fig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], name="Volume"), row=1, col=1)
fig.add_trace(go.Scatter(x=df["date"], y=df["vol_ma_7"], name="7D MA", line=dict(color="orange")), row=1, col=1)

df["vol_ratio"] = df["Volume"] / df["vol_ma_7"]

# OBV and Volume Ratio
fig.add_trace(go.Scatter(x=df["date"], y=df["obv"], name="OBV", line=dict(color="green")), row=2, col=1)
fig.add_trace(go.Scatter(x=df["date"], y=df["vol_ratio"], name="Volume Ratio", line=dict(color="purple", dash="dot")), row=2, col=1)

fig.update_layout(
    title="BTC Volume Analytics",
    height=600,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
