import streamlit as st
import pandas as pd
from data.data_loader import load_motherduck_data
from data.data_loader import get_dataset

# Les paramètres de connexion communs
token_md = st.secrets.get("MOTHERDUCK_TOKEN", "default_token")
database_name = st.secrets.get("MOTHERDUCK_DATABASE", "default_database")
schema_name = st.secrets.get("MOTHERDUCK_SCHEMA", "public")

# Import de "joueurs_par_categorie_evol" depuis MotherDuck
table_name = "joueurs_par_categorie_evol"
@st.cache_data(ttl=3600)  # Mise en cache pour 1 heure
def df_joueurs_par_categorie_evol():
    df_joueurs_par_categorie_evol = load_motherduck_data(token_md, database_name, schema_name, table_name)
    return df_joueurs_par_categorie_evol

# Import de "joueurs_club_saison_precedente_nb" depuis MotherDuck
table_name = "joueurs_club_saison_precedente_nb"
@st.cache_data(ttl=3600)  # Mise en cache pour 1 heure
def df_joueurs_club_saison_precedente_nb():
    df_joueurs_club_saison_precedente_nb = load_motherduck_data(token_md, database_name, schema_name, table_name)
    return df_joueurs_club_saison_precedente_nb

