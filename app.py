# app.py

import streamlit as st

st.set_page_config(page_title="Multi-Page Streamlit App", layout="wide")

st.title("Welcome to My Streamlit App")

st.sidebar.header("Navigation")
st.sidebar.write("Use the sidebar to navigate to Dashboards")

st.write("Please select a page from the sidebar to continue.")
