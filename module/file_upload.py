# modules/file_upload.py

import streamlit as st
import pandas as pd

def read_uploaded_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]

    try:
        if file_type == 'csv':
            df1 = pd.read_csv(uploaded_file)
            df2 = None
            st.success("CSV file successfully loaded.")
            return df1, df2, file_type

        elif file_type in ['xls', 'xlsx']:
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names

            if len(sheet_names) < 2:
                st.warning(f"Only {len(sheet_names)} sheet(s) found. Please upload a file with at least 2 sheets.")
                return None, None, file_type

            df1 = pd.read_excel(xls, sheet_name=sheet_names[0])
            df2 = pd.read_excel(xls, sheet_name=sheet_names[1])

            st.success("Excel file successfully loaded.")
            return df1, df2, file_type

        else:
            st.error("Unsupported file type.")
            return None, None, file_type

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, file_type
