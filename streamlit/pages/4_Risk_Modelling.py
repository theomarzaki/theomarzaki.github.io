import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
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
df['Return'] = df['Close'].pct_change()
returns = df['Return'].dropna()

# Compute CVaR
confidence_level = 0.95
var = returns.quantile(1 - confidence_level)
cvar = returns[returns <= var].mean()

# Bin CVaR values
bins = [-np.inf, -0.05, -0.02, 0]  # Adjust as needed
labels = ['High Risk', 'Medium Risk', 'Low Risk']
df['CVaR'] = df['Return'].rolling(window=30).apply(lambda x: x[x <= x.quantile(1 - confidence_level)].mean(), raw=False)
df['CVaR_bin'] = pd.cut(df['CVaR'], bins=bins, labels=labels)

# Drop NaNs for plotting
plot_df = df.dropna(subset=['CVaR', 'CVaR_bin'])

# --- Plot Distribution ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(returns, bins=50, alpha=0.75, color='skyblue', edgecolor='black')
ax.axvline(x=cvar, color='green', linestyle='--', label=f'CVaR ({confidence_level:.0%})')
ax.text(cvar, ax.get_ylim()[1] * 0.8, f'CVaR\n{cvar:.2%}', color='green', ha='right')

ax.set_title('Distribution of Daily Returns with VaR and CVaR')
ax.set_xlabel('Daily Returns')
ax.set_ylabel('Frequency')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.legend()
st.pyplot(fig)

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
