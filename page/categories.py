import streamlit as st

# --- SETUP PAGE ---
def page_categories():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-bookmark-star"></i> Catégories</h1>
    """, unsafe_allow_html=True)

    # Avertissement
    with st.expander("En cours de développement"):
        st.write("""
        Ce site est encore en cours de développement. Certaines fonctionnalités peuvent ne pas fonctionner comme prévu.
        """)
