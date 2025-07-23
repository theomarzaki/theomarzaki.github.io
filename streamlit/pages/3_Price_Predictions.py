import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ui.sidebar import render_sidebar

render_sidebar()


st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_previous = (current_time - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] < start_of_week_ahead)]
    df.set_index("Date", inplace=True)
    return df


def predict_prices():
    df = pd.read_csv('data/merged_indicators.csv')
    current_time = datetime.utcnow()
    start_of_week_ahead = (current_time).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_ahead)]
    df.set_index("Date", inplace=True)
    return df


def getAccuracy():
    data = pd.read_csv('price_prediction/results/testing_results.csv')
    return data['R2'].values[0]


subpage = st.sidebar.radio("Select: ", ["Price Predictions", "Model Accuracy", "Training Loss"])

if subpage == "Price Predictions":
    st.header("Price Predictions")
    st.title("Model Predictions - 1 Week Ahead")
    df = load_data()
    data = predict_prices()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Actual Close",
        line=dict(color="black")
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        name="Predicted Close",
        line=dict(color="red", dash="dash")
    ))

    fig.update_layout(
        title="BTC Close Price & 7-Day Forecast",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


elif subpage == "Model Accuracy":
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=getAccuracy(),
        number={'suffix': ""},
        title={'text': "Model R² Score"},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "green"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 0.5], 'color': '#f2d7d5'},
                {'range': [0.5, 0.75], 'color': '#fcf3cf'},
                {'range': [0.75, 1.0], 'color': '#d5f5e3'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': getAccuracy()
            }
        }
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


elif subpage == "Training Loss":
    st.header("Training Loss")
    st.write("Show volatility charts here.")
