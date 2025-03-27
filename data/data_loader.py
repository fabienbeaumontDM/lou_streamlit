import duckdb
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)  # Mise en cache pour 1 heure
def load_motherduck_data(token_md, database_name, schema_name, table_name):
    """
    Charge les données depuis MotherDuck avec mise en cache Streamlit
    Args:
        token_md (str): Token d'authentification MotherDuck
        database_name (str): Nom de la base de données
        schema_name (str): Nom du schéma
        table_name (str): Nom de la table à charger
    Returns:
        pandas.DataFrame: DataFrame contenant toutes les données de la table
    """
    try:
        # Établir la connexion
        con_md = duckdb.connect(f"md:{database_name}?motherduck_token={token_md}&saas_mode=true")
        
        # Requête pour sélectionner toutes les colonnes de la table
        query = f"""
        SELECT *
        FROM "{database_name}"."{schema_name}".{table_name}
        """
        
        # Exécuter la requête et convertir en DataFrame
        df = con_md.execute(query).df()
        
        return df
    
    except Exception as e:
        st.sidebar.error(f"Erreur lors du chargement des données : {e}")
        return None

def get_dataset():
    """
    Fonction centralisée pour récupérer le dataset depuis MotherDuck
    Returns:
        pandas.DataFrame: DataFrame chargé
    """
    # Les paramètres de connexion
    TOKEN_MD = st.secrets.get("MOTHERDUCK_TOKEN", "default_token")
    DATABASE_NAME = st.secrets.get("MOTHERDUCK_DATABASE", "default_database")
    SCHEMA_NAME = st.secrets.get("MOTHERDUCK_SCHEMA", "public")
    TABLE_NAME = st.secrets.get("MOTHERDUCK_TABLE", "default_table")
    
    # Charger les données
    df = load_motherduck_data(
        TOKEN_MD, 
        DATABASE_NAME, 
        SCHEMA_NAME, 
        TABLE_NAME
    )
    
    return df