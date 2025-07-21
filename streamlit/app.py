import streamlit as st

st.set_page_config(layout="wide")


st.title("Suggested Actions")

st.sidebar.page_link("app.py", label="Dashboard")
st.sidebar.page_link("pages/1_Indicators.py", label="Indicators")
