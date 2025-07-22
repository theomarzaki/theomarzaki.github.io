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


def verdict_card(title, label, bg_color):
    return f"""
    <div style="
        background-color: {bg_color};
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    ">
        <div style="font-size: 1rem; margin-bottom: 0.5rem;">{title}</div>
        {label}
    </div>
    """


def load_data():
    data = pd.read_csv('data/verdict.csv')
    return data


df = load_data()

tech_label = df[(df['Indicator'] == "Technical")].Verdict.values[0]
market_label = df[(df['Indicator'] == "Market")].Verdict.values[0]
macro_label = df[(df['Indicator'] == "Economic")].Verdict.values[0]
total_label = df[(df['Indicator'] == "Final")].Verdict.values[0]

# Map scores to labels/colors
tech_color = signal_label(tech_label)
market_color = signal_label(market_label)
macro_color = signal_label(macro_label)
total_color = signal_label(total_label)

st.title("BTC Market Suggested Actions Based on Signals")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(verdict_card("Technical", tech_label, tech_color), unsafe_allow_html=True)
with col2:
    st.markdown(verdict_card("Market", market_label, market_color), unsafe_allow_html=True)
with col3:
    st.markdown(verdict_card("Macro", macro_label, macro_color), unsafe_allow_html=True)
with col4:
    st.markdown(verdict_card("Final", total_label, total_color), unsafe_allow_html=True)
