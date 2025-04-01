import streamlit as st
import plotly.express as px
from utils.calculations_old import data_analyzer

# --- SETUP PAGE ---
def page_clubs():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-award"></i> Clubs</h1>
    """, unsafe_allow_html=True)
    
    # Distribution des clubs
    distribution = data_analyzer.get_clubs_distribution()
    
    if distribution is not None:
        st.dataframe(distribution)
        
        # Graphique de distribution des clubs
        fig = px.bar(
            x=distribution.index, 
            y=distribution.values, 
            title='Distribution des Clubs'
        )
        st.plotly_chart(fig)

