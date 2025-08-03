import streamlit as st
from ui.sidebar import render_sidebar
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

render_sidebar()

st.set_page_config(layout="wide")


st.title("Sentiment Analysis")

df = pd.read_csv('data/merged_indicators.csv')

# Make sure Date is datetime
df['Date'] = pd.to_datetime(df['Date'])

current_time = datetime.utcnow()
start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
start_of_week_ahead = (current_time).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
df = df.drop_duplicates(subset=['Date'])


# Create figure with secondary y-axis
fig = go.Figure()

# Add BTC price trace
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Close'],
    name='BTC Price',
    line=dict(color='blue'),
    yaxis='y1'
))

# Add sentiment trace
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Sentiment'],
    name='Sentiment Score',
    line=dict(color='orange', dash='dot'),
    yaxis='y2'
))

# Update layout with dual axes
fig.update_layout(
    title='BTC Price vs Sentiment Over Time',
    xaxis=dict(title='Date'),
    yaxis=dict(title='BTC Price (USD)', side='left'),
    yaxis2=dict(title='Sentiment', overlaying='y', side='right'),
    legend=dict(x=0, y=1),
    height=500,
    margin=dict(l=60, r=60, t=40, b=40)
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
