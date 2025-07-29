import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
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

confidence_level = 95

fig, ax = plt.subplots(figsize=(10, 6))

# Histogram of returns
ax.hist(returns, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# Add VaR and CVaR lines
ax.axvline(x=cvar, color='green', linestyle='--', label=f'CVaR ({confidence_level:.0%})')

# Annotate lines
ax.text(cvar, ax.get_ylim()[1] * 0.8, f'CVaR\n{cvar:.2%}', color='green', ha='right')

# Labels and formatting
ax.set_title('Distribution of Daily Returns with VaR and CVaR')
ax.set_xlabel('Daily Returns')
ax.set_ylabel('Frequency')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.legend()

# Display in Streamlit
st.pyplot(fig)

latest_cvar = df[['Date', 'CVaR', 'CVaR_bin']].dropna().sort_values('Date').tail(3)

st.subheader("ecent CVaR Risk Snapshots")

for _, row in latest_cvar.iterrows():
    date_str = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
    cvar_pct = f"{row['CVaR'] * 100:.2f}%"
    risk = row['CVaR_bin']
    st.markdown(f"""
    <div style='padding: 10px; margin-bottom: 8px; background-color: #f9f9f9; border-left: 6px solid #888; font-size: 0.95rem;'>
        <strong>date_str}</strong> &nbsp; | &nbsp;
        <strong>CVaR:</strong> {cvar_pct} &nbsp; | &nbsp;
        <strong>Risk:</strong> {risk}
    </div>
    """, unsafe_allow_html=True)
