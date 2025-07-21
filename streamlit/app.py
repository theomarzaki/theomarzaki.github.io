import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/predictions.py", label="📈 Predictions")
st.sidebar.page_link("pages/performance.py", label="📊 Performance")
st.sidebar.page_link("pages/indicators.py", label="📉 Indicators")
