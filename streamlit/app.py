import streamlit as st

st.set_page_config(layout="wide")


# Sidebar navigation
st.sidebar.title("📊 BTC Dashboard")
page = st.sidebar.radio("Go to", ["Home", "Predictions", "Performance", "Indicators"])

# Routing logic
if page == "Home":
    st.title("🏠 Bitcoin Prediction Dashboard")
    st.write("Welcome to the BTC LSTM prediction dashboard.")

elif page == "Predictions":
    # You can import or define this page's content here
    st.title("📈 LSTM Predictions")
    # load predictions and chart

elif page == "Performance":
    st.title("📊 Performance & PnL")
    # load performance metrics

elif page == "Indicators":
    st.title("📉 Technical Indicators")
    # render indicators
