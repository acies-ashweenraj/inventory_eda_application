import streamlit as st
from module.file_upload import read_uploaded_file

st.title("Dashboard 1 - File Upload")

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    df1, df2, file_type = read_uploaded_file(uploaded_file)

    if df1 is not None:
        st.subheader("DataFrame 1")
        st.dataframe(df1.head())

    if df2 is not None:
        st.subheader("DataFrame 2")
        st.dataframe(df2.head())
    
    # Order stats
    order_summary = df1.groupby('SKU ID')['Order Quantity'].agg(['sum', 'mean', 'std', 'count']).reset_index()
    order_summary.columns = ['SKU ID', 'Total Orders', 'Avg Order Qty', 'STD Order Qty', 'Order Count']

    # Merge with stock
    merged_df = df2.merge(order_summary, on='SKU ID', how='left').fillna(0)
    st.session_state['merged_df'] = merged_df

