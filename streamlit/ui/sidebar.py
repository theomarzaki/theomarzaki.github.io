import streamlit as st


def render_sidebar():
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Indicators.py", label="Indicators")
    st.sidebar.page_link("pages/2_Volume.py", label="Volume")
    st.sidebar.page_link("pages/3_Price_Predictions.py", label="Price Predictions")
    st.sidebar.page_link("pages/4_Risk_Modelling.py", label="Risk Modelling")
    st.sidebar.page_link("pages/5_Trader", label="Asset Trader")
