import streamlit as st
from ui.sidebar import render_sidebar
import pandas as pd
import plotly.express as px
import numpy as np

render_sidebar()

st.set_page_config(layout="wide")


st.title("Risk Modelling")

df = pd.read_csv('data/merged_indicators.csv')

bins = [-np.inf, -0.05, -0.02, 0]  # Very risky, moderate, mild
labels = ['High Risk', 'Medium Risk', 'Low Risk']

df['CVaR_bin'] = pd.cut(df['CVaR'], bins=bins, labels=labels)

# Drop NaNs for clean plotting
plot_df = df.dropna(subset=['CVaR', 'CVaR_bin'])

fig = px.scatter(
    plot_df,
    x='Date',
    y='CVaR',
    color='CVaR_bin',
    color_discrete_map={
        'High Risk': 'red',
        'Medium Risk': 'orange',
        'Low Risk': 'green'
    },
    title='Binned 30-Day Rolling CVaR',
    labels={'CVaR': 'CVaR', 'CVaR_bin': 'Risk Level'},
)

fig.update_layout(
    height=400,
    template='plotly_white',
    margin=dict(l=30, r=30, t=50, b=30)
)


st.plotly_chart(fig, use_container_width=True)

latest_cvar = df[['Date', 'CVaR', 'CVaR_bin']].dropna().sort_values('Date').tail(3)

st.subheader("Recent CVaR Risk Snapshots")

for _, row in latest_cvar.iterrows():
    date_str = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
    cvar_pct = f"{row['CVaR'] * 100:.2f}%"
    risk = row['CVaR_bin']
    st.markdown(f"""
    <div style='padding: 10px; margin-bottom: 8px; background-color: #f9f9f9; border-left: 6px solid #888; font-size: 0.95rem;'>
        <strong>{date_str}</strong> &nbsp; | &nbsp;
        <strong>CVaR:</strong> {cvar_pct} &nbsp; | &nbsp;
        <strong>Risk:</strong> {risk}
    </div>
    """, unsafe_allow_html=True)
