import streamlit as st
from utils.calculations_old import data_analyzer

# --- SETUP PAGE ---
def page_categories():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-bookmark-star"></i> Catégories</h1>
    """, unsafe_allow_html=True)

    # Distribution des catégories
    distribution = data_analyzer.get_categories_distribution()
    
    if distribution is not None:
        st.dataframe(distribution)
        
        # Graphique de distribution
        fig = data_analyzer.create_category_chart()
        if fig:
            st.plotly_chart(fig)

