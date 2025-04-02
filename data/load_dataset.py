import streamlit as st
import pandas as pd
from utils.data_loader import load_motherduck_data

# Paramètres de connexion communs
token_md = st.secrets.get("MOTHERDUCK_TOKEN", "default_token")
database_name = st.secrets.get("MOTHERDUCK_DATABASE", "default_database")
schema_name = st.secrets.get("MOTHERDUCK_SCHEMA", "public")

@st.cache_data(ttl=3600)  # Mise en cache pour 1 heure
def load_joueurs_par_categorie_evol():
    table_name = "joueurs_par_categorie_evol"
    return load_motherduck_data(token_md, database_name, schema_name, table_name)

@st.cache_data(ttl=3600)
def load_joueurs_club_saison_precedente_detail_nb():
    table_name = "joueurs_club_saison_precedente_detail_nb"
    return load_motherduck_data(token_md, database_name, schema_name, table_name)

@st.cache_data(ttl=3600)
def load_joueurs_club_saison_precedente_nb():
    table_name = "joueurs_club_saison_precedente_nb"
    return load_motherduck_data(token_md, database_name, schema_name, table_name)
