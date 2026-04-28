import streamlit as st
import pandas as pd
import os

st.title("Debug Test")

csv_files = [
    'powerbi_01_spending_trends.csv',
    'powerbi_02_insurance_gap.csv',
    'powerbi_03_telemedicine_adoption.csv',
    'powerbi_04_startup_ecosystem.csv',
    'powerbi_05_vc_misalignment.csv',
    'powerbi_06_segment_comparison.csv',
    'powerbi_07_kpi_metrics.csv',
    'powerbi_08_company_details.csv'
]

st.write("Checking for CSV files...")

for file in csv_files:
    if os.path.exists(file):
        st.write(f"✅ {file} - FOUND")
    else:
        st.write(f"❌ {file} - NOT FOUND")

st.write("Current directory:", os.getcwd())
st.write("Files in directory:", os.listdir())
