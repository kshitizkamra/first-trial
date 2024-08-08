import streamlit as st

# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('marketplace_analysis_db', type='sql')

conn
