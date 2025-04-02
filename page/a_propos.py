import streamlit as st

# --- SETUP PAGE ---
def page_a_propos():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-info-circle"></i> A propos</h1>
    """, unsafe_allow_html=True)
    st.write("""
    ## Informations sur l'Application
    
    Cette application est un POC afin d'avoir des analyses
    sur la population des joueurs du LOU Rugby des catégories jeunes.
             
    L'application est en cours de développement.
    
    ## Technologies Utilisées
    - Streamlit
    - Pandas
    - Numpy
    - DuckDB / Motherduck
    - streamlit-folium
    """)

