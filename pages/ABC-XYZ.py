# pages/2_ABC_XYZ_Analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# You should receive df1 from session state or directly in this page
if 'df1' not in st.session_state:
    st.warning("Please upload file first in Dashboard 1.")
    st.stop()

df = st.session_state['df1'].copy()

st.title("ABC-XYZ Inventory Classification")

# -- ABC Classification --

# Calculate Consumption Value
df['Consumption Value'] = df['Total Orders'] * df['Unit Price']
df = df.sort_values('Consumption Value', ascending=False)
df['Cumulative %'] = 100 * df['Consumption Value'].cumsum() / df['Consumption Value'].sum()

def classify_abc(cum_pct):
    if cum_pct <= 70:
        return 'A'
    elif cum_pct <= 90:
        return 'B'
    else:
        return 'C'

df['ABC Class'] = df['Cumulative %'].apply(classify_abc)

# -- XYZ Classification --

df['CV'] = df['STD Order Qty'] / (df['Avg Order Qty'] + 1e-9)

def classify_xyz(cv):
    if cv <= 0.5:
        return 'X'
    elif cv <= 1:
        return 'Y'
    else:
        return 'Z'

df['XYZ Class'] = df['CV'].apply(classify_xyz)
df['ABC-XYZ Class'] = df['ABC Class'] + "-" + df['XYZ Class']

st.subheader("ABC-XYZ Classified Data")
st.dataframe(df[['SKU ID', 'ABC Class', 'XYZ Class', 'ABC-XYZ Class', 'Total Orders', 'Order Count', 'STD Order Qty']])

# -- Heatmap --

abc_xyz_df = df[['SKU ID', 'ABC Class', 'XYZ Class']].copy()
heatmap_data = abc_xyz_df.groupby(['ABC Class', 'XYZ Class']).size().reset_index(name='Count')
pivot_df = heatmap_data.pivot(index='XYZ Class', columns='ABC Class', values='Count').fillna(0)

fig = go.Figure(data=go.Heatmap(
    z=pivot_df.values,
    x=pivot_df.columns,
    y=pivot_df.index,
    colorscale='Plasma',
    colorbar=dict(title='Number of SKUs'),
    showscale=True
))

annotations = []
for i, y_val in enumerate(pivot_df.index):
    for j, x_val in enumerate(pivot_df.columns):
        annotations.append(
            dict(
                x=x_val,
                y=y_val,
                text=str(int(pivot_df.iloc[i, j])),
                showarrow=False,
                font=dict(
                    color='white' if pivot_df.iloc[i, j] > pivot_df.values.max()/2 else 'black',
                    size=16
                )
            )
        )

fig.update_layout(
    title='ABC-XYZ Matrix (Count of SKUs)',
    xaxis_title='ABC Class',
    yaxis_title='XYZ Class',
    annotations=annotations,
    xaxis=dict(tickmode='array', tickvals=pivot_df.columns, ticktext=pivot_df.columns),
    yaxis=dict(tickmode='array', tickvals=pivot_df.index, ticktext=pivot_df.index),
    font=dict(size=16)
)

st.subheader("ABC-XYZ Heatmap")
st.plotly_chart(fig, use_container_width=True)
