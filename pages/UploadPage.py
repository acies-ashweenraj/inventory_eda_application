import streamlit as st
from module.file_upload import read_uploaded_file

st.title("Dashboard 1 - File Upload")

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    df1, df2, file_type = read_uploaded_file(uploaded_file)

    if df1 is not None:
        st.subheader("DataFrame 1")
        st.dataframe(df1)

    if df2 is not None:
        st.subheader("DataFrame 2")
        st.dataframe(df2)
