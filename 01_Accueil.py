import streamlit as st
import pandas as pd
import duckdb as db

# --- VARIABLES ---
token_md = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZhYmllbi5iZWF1bW9udEBkYXRhLW1ham9yLmNvbSIsInNlc3Npb24iOiJmYWJpZW4uYmVhdW1vbnQuZGF0YS1tYWpvci5jb20iLCJwYXQiOiJGY0NtRUg1STRMMENYWDgyT2RtamlWYmJlanI2RGRYdHVYY3RHUkhPcHFvIiwidXNlcklkIjoiMDBlMjQzMGEtODZhYi00NTg2LWI2NzUtZjIxNDdlNzA2NDQ1IiwiaXNzIjoibWRfcGF0IiwicmVhZE9ubHkiOmZhbHNlLCJ0b2tlblR5cGUiOiJyZWFkX3dyaXRlIiwiaWF0IjoxNzQzMDAyMTUzfQ.qxsoRrVYIwPd9YZVo6zKg2Ad8AMj0risog2fdb3TCK8"
database_name = f"lou_poc"
schema_name = f"4_gold"

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="LOU Rugby - Accueil",
    page_icon=":rugby_football:",
    layout="wide")

# --- SETUP PAGE ---
st.title("Accueil")
st.write("Bienvenue sur l'application du LOU Rugby")
st.write("Vous trouverez ci-dessous les principaux indicateurs des équipes pour la saison 2024-2025")

# --- CONNEXION BDD ---
# token_md = st.secrets["token_md"]
# database_name = st.secrets["database_name"]
# schema_name = st.secrets["schema_name"]

con_md = db.connect("md:lou_poc?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZhYmllbi5iZWF1bW9udEBkYXRhLW1ham9yLmNvbSIsInNlc3Npb24iOiJmYWJpZW4uYmVhdW1vbnQuZGF0YS1tYWpvci5jb20iLCJwYXQiOiJGY0NtRUg1STRMMENYWDgyT2RtamlWYmJlanI2RGRYdHVYY3RHUkhPcHFvIiwidXNlcklkIjoiMDBlMjQzMGEtODZhYi00NTg2LWI2NzUtZjIxNDdlNzA2NDQ1IiwiaXNzIjoibWRfcGF0IiwicmVhZE9ubHkiOmZhbHNlLCJ0b2tlblR5cGUiOiJyZWFkX3dyaXRlIiwiaWF0IjoxNzQzMDAyMTUzfQ.qxsoRrVYIwPd9YZVo6zKg2Ad8AMj0risog2fdb3TCK8&saas_mode=true")
# con = db.connect(database="md:{database_name}?motherduck_token={token_md}", read_only=True)
# con = db.connect("md:[{database_name}]?motherduck_token=[{token_md}]&saas_mode=true")

# --- DATASET ---
@st.cache_data
def get_data():
    query = f"""
    SELECT 
        *
    FROM lou_poc."4_gold".fact_joueur
    """
    return con_md.execute(query).df()

# --- DATA ---
df = pd.DataFrame(get_data())
# Connexion à DuckDB pour calcul d'indicateurs et charger le DataFrame dans DuckDB
con = db.connect(database=':memory:')
con.execute("CREATE TABLE dataset AS SELECT * FROM df")

# --- METRIC ---
# Calculer les indicateurs
q_nb_joueurs_categorie_current_saison = """
SELECT 0 AS CD_CATEGORIE, 'Nombre de joueurs total' AS LB_CATEGORIE, COUNT(ID_JOUEUR) AS NB
FROM dataset
WHERE CD_SAISON = '2024-2025' AND LB_NOM_CLUB = 'LYON OL U'
UNION
SELECT CD_CATEGORIE, LB_CATEGORIE, COUNT(ID_JOUEUR) AS NB
FROM dataset
WHERE CD_SAISON = '2024-2025' AND LB_NOM_CLUB = 'LYON OL U'
GROUP BY CD_CATEGORIE, LB_CATEGORIE
ORDER BY CD_CATEGORIE
"""
res_nb_joueurs_categorie_current_saison = con.execute(q_nb_joueurs_categorie_current_saison).fetchdf()



# --- PAGE CONTENT ---
# KPI haut de page
with st.container():
    cols = st.columns(5)
    for index, row in res_nb_joueurs_categorie_current_saison.iterrows():
        col = cols[index % 5]
        with col:
            st.metric(label=row['LB_CATEGORIE'], value=f"{row['NB']}", border=True)

# kpi_col1.metric(label="Nombre de joueurs total", value=res_nb_joueurs_categorie_current_saison['NB'].sum(), border=True)
# kpi_col2.metric(label="Nombre de joueurs Moins de 15 ans", value=nb_de_joueurs_15ans['NB'].sum(), border=True)
# kpi_col3.metric(label="Nombre de joueurs Moins de 16 ans", value=nb_de_joueurs_16ans['NB'].sum(), border=True)
# kpi_col4.metric(label="Nombre de joueurs Moins de 18 ans", value=nb_de_joueurs_18ans['NB'].sum(), border=True)
# kpi_col5.metric(label="Nombre de joueurs 18 ans et plus", value=nb_de_joueurs_18ansplus['NB'].sum(), border=True)

