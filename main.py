import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Configuration de la page
st.set_page_config(
    page_title="LOU Rugby - POC",
    page_icon="🏉",
    layout="wide"
)

# Importer toutes les pages
from page.accueil import page_accueil
from page.categories import page_categories
from page.annees import page_annees
from page.clubs import page_clubs
from page.joueurs import page_joueurs
from page.a_propos import page_a_propos
from page.contact import page_contact

# Fonction pour afficher une image dans la sidebar
def sidebar_logo(expanded):
    logo_path = "images/logo-lou-rugby-long.png" if expanded else "images/logo-lou-rugby.png"
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    return f'<img src="data:image/png;base64,{img_base64}" style="width:100%; margin-bottom:10px;">'

def main():
    # Style CSS personnalisé pour la sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #e8e8e8 !important;
            }
            [data-testid="stSidebarNav"] button {
                background: url('images/logo-lou-rugby.png') no-repeat center center !important;
                background-size: contain !important;
                width: 50px !important;
                height: 50px !important;
                border: none !important;
            }
            button[kind="icon"] {
                background: url('images/logo-lou-rugby.png') no-repeat center center !important;
                background-size: contain !important;
                width: 50px !important;
                height: 50px !important;
                border: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        # Ajout du logo en fonction de l'état de la barre latérale
        expanded = st.session_state.get("sidebar_expanded", True)
        st.markdown(sidebar_logo(expanded), unsafe_allow_html=True)
        
        # Menu principal
        selected_page = option_menu(
            menu_title=None,  # Pas de titre
            options=["Accueil", "Catégories", "Années", "Clubs", "Joueurs", "À Propos", "Contact"],
            icons=["house", "bookmark-star", "calendar3", "award", "people", "info-circle", "envelope"],
            menu_icon=None,
            default_index=0
        )
        
    # Routing des pages
    if selected_page == "Accueil":
        page_accueil()
    elif selected_page == "Catégories":
        page_categories()
    elif selected_page == "Années":
        page_annees()
    elif selected_page == "Clubs":
        page_clubs()
    elif selected_page == "Joueurs":
        page_joueurs()
    elif selected_page == "À Propos":
        page_a_propos()
    elif selected_page == "Contact":
        page_contact()

if __name__ == "__main__":
    main()
