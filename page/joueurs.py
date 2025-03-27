import streamlit as st
import plotly.express as px
from utils.calculations import data_analyzer

# --- SETUP PAGE ---
def page_joueurs():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-people"></i> Joueurs</h1>
    """, unsafe_allow_html=True)
    
    # Distribution des joueurs
    distribution = data_analyzer.get_players_distribution()
    
    if distribution is not None:
        st.dataframe(distribution)
        
        # Graphique des top joueurs
        top_joueurs = distribution.head(10)
        fig = px.bar(
            x=top_joueurs.index, 
            y=top_joueurs.values, 
            title='Top 10 Joueurs'
        )
        st.plotly_chart(fig)