import streamlit as st
import streamlit_antd_components as sac

# --- SETUP PAGE ---
def page_clubs():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-award"></i> Clubs</h1>
    """, unsafe_allow_html=True)
    
    # Avertissement
    sac.alert(label='En construction',
              description='Ce site est encore en cours de développement. Certaines fonctionnalités peuvent ne pas fonctionner comme prévu.',
              size='lg',
              radius='lg',
              variant='filled',
              color='red',
              banner=True,
              icon=True,
              closable=True)
