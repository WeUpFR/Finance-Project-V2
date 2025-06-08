import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.loader import load_trial_balance
from src.mapping import load_mapping_template
from src.statements import build_financial_statements
from src.formatter import format_and_export_excel
from src.pdf_export import export_to_pdf

def run_ui():
    """
    Initializes and runs the Streamlit web user interface.
    """
    st.set_page_config(page_title="Demerara Financial Reporter", layout="wide")
    
    st.title("Demerara Life Financial Reporter")
    st.write("Upload a trial balance Excel or CSV file to generate financial statements.")

    if 'ready_to_download' not in st.session_state:
        st.session_state['ready_to_download'] = False

    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'xls', 'csv'])

    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        temp_dir = "temp_streamlit"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        mapping_path = "mapping_template.json"
        
        if st.button("Generate Financial Statements"):
            with st.spinner("Processing..."):
                tb_df = load_trial_balance(file_path)
                mapping = load_mapping_template(mapping_path)
                
                if not tb_df.empty and mapping:
                    statements = build_financial_statements(tb_df, mapping)
                    st.session_state['statements'] = statements
                    st.session_state['ready_to_download'] = True
                    st.success("Financial statements generated!")
                else:
                    st.error("Failed to process files. Please check the logs.")

    if st.session_state.get('ready_to_download'):
        st.header("Generated Reports")
        statements = st.session_state['statements']
        
        for name, df in statements.items():
            if not df.empty and not df.iloc[0,0].startswith('Cash flow'):
                st.subheader(name)
                st.dataframe(df.style.format({'Amount': "{:,.2f}"}, na_rep=""))
        
        st.subheader("Download Reports")
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        excel_path = os.path.join(output_dir, "financial_statements.xlsx")
        format_and_export_excel(statements, excel_path)
        with open(excel_path, "rb") as file:
            st.download_button("Download as Excel", file, "financial_statements.xlsx")

        pdf_path = os.path.join(output_dir, "financial_statements.pdf")
        export_to_pdf(statements, pdf_path)
        with open(pdf_path, "rb") as file:
            st.download_button("Download as PDF", file, "financial_statements.pdf")
