import streamlit as st
import plotly.express as px
from utils.calculations import data_analyzer

# --- SETUP PAGE ---
def page_annees():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-calendar3"></i> Années</h1>
    """, unsafe_allow_html=True)
    
    # Distribution par années
    distribution = data_analyzer.get_years_distribution()
    
    if distribution is not None:
        st.dataframe(distribution)
        
        # Graphique de distribution
        fig = data_analyzer.create_years_chart()
        if fig:
            st.plotly_chart(fig)
