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
    start_of_week_previous = (current_time - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
    df = df[(df['Date'] > start_of_week_previous) & (df['Date'] <= start_of_week_ahead)]
    df.set_index("Date", inplace=True)
    return df


def predict_prices():
    df = pd.read_csv('price_prediction/results/price_predictions.csv', index_col=0)
    current_time = datetime.utcnow()
    current_time = (current_time - timedelta(days=1))
    future_dates = [current_time + timedelta(days=i) for i in range(1, 8)]

    # build prediction DataFrame
    pred_df = pd.DataFrame({
        "Date": pd.to_datetime(future_dates),
        "predicted_close": df['0']
    })

    pred_df["Date"] = pd.to_datetime(pred_df["Date"]).dt.strftime("%Y-%m-%d")
    pred_df.set_index("Date", inplace=True)
    return pred_df


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
# fig.add_trace(go.Scatter(
#     x=data.index,
#     y=data["predicted_close"],
#     name="Predicted Close",
#     line=dict(color="red", dash="dash")
# ))

fig.update_layout(
    title="BTC Close Price & 7-Day Forecast",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_white",
    height=500
)

# Streamlit render
st.plotly_chart(fig, use_container_width=True)
