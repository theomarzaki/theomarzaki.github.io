import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ui.sidebar import render_sidebar

render_sidebar()


st.set_page_config(layout="wide")
st.title("Model Predictions - 1 Week Ahead")


@st.cache_data
def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
    df.set_index("Date", inplace=True)
    return df


df = load_data()


fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line=dict(color="black")))

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
