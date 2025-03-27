import streamlit as st
from utils.calculations import data_analyzer

# --- SETUP PAGE ---
def page_accueil():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-house"></i> Accueil</h1>
    """, unsafe_allow_html=True)
    
    st.write("""
    Bienvenue sur l'application du LOU Rugby.
    
    Vous trouverez ci-dessous les principaux indicateurs des équipes pour la saison 2024-2025.
    
    """)
    
    # Exemple de graphiques sur la page d'accueil
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des Catégories")
        fig_categories = data_analyzer.create_category_chart()
        if fig_categories:
            st.plotly_chart(fig_categories)
    
    with col2:
        st.subheader("Distribution par Années")
        fig_years = data_analyzer.create_years_chart()
        if fig_years:
            st.plotly_chart(fig_years)

