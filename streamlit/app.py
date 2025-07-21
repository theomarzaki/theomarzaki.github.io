import streamlit as st

st.set_page_config(layout="wide")


# Get current page from URL query param
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

# Sidebar menu
st.sidebar.title("📊 BTC Dashboard")

st.sidebar.markdown("### Navigation")
st.sidebar.markdown(f"""
- [{emoji('🏠')} Home](?page=Home)
- [{emoji('📈')} Predictions](?page=Predictions)
- [{emoji('📊')} Performance](?page=Performance)
- [{emoji('📉')} Indicators](?page=Indicators)
""", unsafe_allow_html=True)

# Page content
if page == "Home":
    st.title("🏠 Bitcoin Prediction Dashboard")
    st.write("Welcome to the BTC LSTM prediction dashboard.")

elif page == "Predictions":
    st.title("📈 LSTM Predictions")
    # predictions content here

elif page == "Performance":
    st.title("📊 Performance & PnL")
    # performance metrics

elif page == "Indicators":
    st.title("📉 Technical Indicators")
    # indicators content here

else:
    st.error("Page not found.")
