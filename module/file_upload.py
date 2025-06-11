# modules/file_upload.py

import streamlit as st
import pandas as pd

def read_uploaded_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]

    try:
        if file_type == 'csv':
            order_df = pd.read_csv(uploaded_file)
            stock_df = None
            st.success("CSV file successfully loaded.")
            return order_df, stock_df, file_type

        elif file_type in ['xls', 'xlsx']:
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names

            if len(sheet_names) < 2:
                st.warning(f"Only {len(sheet_names)} sheet(s) found. Please upload a file with at least 2 sheets.")
                return None, None, file_type

            order_df = pd.read_excel(xls, sheet_name=sheet_names[0])
            stock_df = pd.read_excel(xls, sheet_name=sheet_names[1])

            order_df['Order Date'] = pd.to_datetime(order_df['Order Date'], dayfirst=True)

            # Standardize column names
            order_df.columns = order_df.columns.str.strip()
            stock_df.columns = stock_df.columns.str.strip()
            
            st.success("Excel file successfully loaded.")
            return order_df, stock_df, file_type

        else:
            st.error("Unsupported file type.")
            return None, None, file_type

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, file_type
