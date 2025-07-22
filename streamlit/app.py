import streamlit as st
from ui.sidebar import render_sidebar
import pandas as pd

render_sidebar()
st.set_page_config(layout="wide")


def signal_label(signal):
    if signal == "Buy":
        return "green"
    elif signal == "Sell":
        return "red"
    else:
        return "orange"


def load_data():
    data = pd.read_csv('data/verdict.csv')
    return data


df = load_data()

tech_verdict = df[(df['Indicator'] == "Technical")].Verdict.values[0]
market_verdict = df[(df['Indicator'] == "Market")].Verdict.values[0]
macro_verdict = df[(df['Indicator'] == "Economic")].Verdict.values[0]
total_verdict = df[(df['Indicator'] == "Final")].Verdict.values[0]

# Map scores to labels/colors
tech_color = signal_label(tech_verdict)
market_color = signal_label(market_verdict)
macro_color = signal_label(macro_verdict)
total_color = signal_label(total_verdict)

st.title("BTC Market Signal Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("#### 📈 Technical")
    st.markdown(f"<div style='color:{tech_color}; font-size:32px; font-weight:bold'>{tech_verdict}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("#### 🏦 Market Sentiment")
    st.markdown(f"<div style='color:{market_color}; font-size:32px; font-weight:bold'>{market_verdict}</div>", unsafe_allow_html=True)

with col3:
    st.markdown("#### 🌐 Macro")
    st.markdown(f"<div style='color:{macro_color}; font-size:32px; font-weight:bold'>{macro_verdict}</div>", unsafe_allow_html=True)

with col4:
    st.markdown("#### 📊 Final Suggestion")
    st.markdown(f"<div style='color:{total_color}; font-size:36px; font-weight:bold'>{total_verdict}</div>", unsafe_allow_html=True)
