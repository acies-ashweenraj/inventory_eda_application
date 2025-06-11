import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("Dashboard 2 - ABC-XYZ Analysis")

# Check if merged_df is available (assuming you're storing merged_df in session state from Dashboard 1)
if 'merged_df' not in st.session_state:
    st.warning("Please upload and process file in Dashboard 1 first.")
    st.stop()

merged_df = st.session_state['merged_df'].copy()

st.subheader("Merged Data")
st.dataframe(merged_df.head())

# Validate required columns
required_cols = ['SKU ID', 'Total Orders', 'Avg Order Qty', 'STD Order Qty', 'Unit Price']
missing_cols = [col for col in required_cols if col not in merged_df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

# ---------------------------------------------------
# Step 1 — ABC Classification (based on consumption value)
# ---------------------------------------------------
merged_df['Consumption Value'] = merged_df['Total Orders'] * merged_df['Unit Price']
merged_df = merged_df.sort_values('Consumption Value', ascending=False)
merged_df['Cumulative %'] = 100 * merged_df['Consumption Value'].cumsum() / merged_df['Consumption Value'].sum()

def classify_abc(cum_pct):
    if cum_pct <= 70:
        return 'A'
    elif cum_pct <= 90:
        return 'B'
    else:
        return 'C'

merged_df['ABC Class'] = merged_df['Cumulative %'].apply(classify_abc)

# ---------------------------------------------------
# Step 2 — XYZ Classification (based on coefficient of variation)
# ---------------------------------------------------
merged_df['CV'] = merged_df['STD Order Qty'] / (merged_df['Avg Order Qty'] + 1e-9)

def classify_xyz(cv):
    if cv <= 0.5:
        return 'X'
    elif cv <= 1:
        return 'Y'
    else:
        return 'Z'

merged_df['XYZ Class'] = merged_df['CV'].apply(classify_xyz)

# ---------------------------------------------------
# Step 3 — Combine ABC & XYZ
# ---------------------------------------------------
merged_df['ABC-XYZ Class'] = merged_df['ABC Class'] + "-" + merged_df['XYZ Class']

# ---------------------------------------------------
# Step 4 — Show ABC-XYZ classified data
# ---------------------------------------------------
st.subheader("ABC-XYZ Classified Data")
st.dataframe(merged_df[['SKU ID', 'ABC Class', 'XYZ Class', 'ABC-XYZ Class', 
                        'Total Orders', 'Avg Order Qty', 'STD Order Qty', 
                        'Order Count', 'Unit Price']])

# ---------------------------------------------------
# Step 5 — ABC-XYZ Heatmap
# ---------------------------------------------------
st.subheader("ABC-XYZ Heatmap")

abc_xyz_df = merged_df.groupby(['ABC Class', 'XYZ Class']).size().reset_index(name='Count')
pivot_df = abc_xyz_df.pivot(index='XYZ Class', columns='ABC Class', values='Count').fillna(0)

fig = go.Figure(data=go.Heatmap(
    z=pivot_df.values,
    x=pivot_df.columns,
    y=pivot_df.index,
    colorscale='Plasma',
    colorbar=dict(title='Number of SKUs'),
    showscale=True
))

# Add annotation text
annotations = []
for i, y_val in enumerate(pivot_df.index):
    for j, x_val in enumerate(pivot_df.columns):
        annotations.append(
            dict(
                x=x_val,
                y=y_val,
                text=str(int(pivot_df.iloc[i, j])),
                showarrow=False,
                font=dict(color='white' if pivot_df.iloc[i, j] > pivot_df.values.max()/2 else 'black', size=14)
            )
        )

fig.update_layout(
    title='ABC-XYZ Matrix (Count of SKUs)',
    xaxis_title='ABC Class',
    yaxis_title='XYZ Class',
    annotations=annotations,
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)
