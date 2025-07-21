import streamlit as st
from ui.sidebar import render_sidebar

render_sidebar()
st.set_page_config(layout="wide", page_title="Home")
