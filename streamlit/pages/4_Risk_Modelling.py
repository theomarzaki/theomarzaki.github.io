import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from ui.sidebar import render_sidebar

# --- Setup ---
st.set_page_config(layout="wide")
render_sidebar()
st.title("Risk Modelling")

# --- Load and Prepare Data ---
df = pd.read_csv('data/merged_indicators.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Compute returns
returns = df['Return'].dropna()

# Compute CVaR
confidence_level = 0.95
var = returns.quantile(1 - confidence_level)
cvar = returns[returns <= var].mean()
df['CVaR'] = cvar

# Bin CVaR values
bins = [-np.inf, -0.05, -0.02, 0]  # Adjust as needed
labels = ['High Risk', 'Medium Risk', 'Low Risk']
df['CVaR_bin'] = pd.cut(df['CVaR'], bins=bins, labels=labels)

# Drop NaNs for plotting
plot_df = df.dropna(subset=['CVaR', 'CVaR_bin'])

# --- Plot Distribution ---
fig = go.Figure()

# Histogram
fig.add_trace(go.Histogram(
    x=returns,
    nbinsx=50,
    marker_color='skyblue',
    name='Returns',
    opacity=0.75
))

# CVaR line
fig.add_vline(x=cvar, line_dash='dash', line_color='green',
              annotation_text=f'CVaR ({confidence_level:.0%})', annotation_position='top right')

fig.update_layout(
    title='Distribution of Daily Returns with CVaR',
    xaxis_title='Daily Returns',
    yaxis_title='Frequency',
    bargap=0.05
)

st.plotly_chart(fig, use_container_width=True)

# --- Display Recent Snapshots ---
st.subheader("Recent CVaR Risk Snapshots")

latest_cvar = df[['Date', 'CVaR', 'CVaR_bin']].dropna().sort_values('Date').tail(3)

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
