import streamlit as st
from utils.data_loader import get_dataset

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="LOU Rugby - Accueil",
    page_icon=":rugby_football:",
    layout="wide")

def main():
    # --- SETUP PAGE ---
    st.title("Accueil")
    st.write("Bienvenue sur l'application du LOU Rugby")
    st.write("Vous trouverez ci-dessous les principaux indicateurs des équipes pour la saison 2024-2025")
    
    # --- DATASET ---
    df = get_dataset()
    
    # --- DATA ---
    if df is not None:
        # --- PAGE CONTENT ---
        # KPI haut de page
        with st.container():
            cols = st.columns(5)
            for index, row in res_nb_joueurs_categorie_current_saison.iterrows():
                col = cols[index % 5]
                with col:
                    st.metric(label=row['LB_CATEGORIE'], value=f"{row['NB']}", border=True)


        # Exemple de visualisation
        st.subheader("Aperçu des Données")
        st.dataframe(df.head())
        
        # Exemple de sidebar avec des filtres
        st.sidebar.header("Filtres")
        
        # Exemples de filtres dynamiques
        colonnes_numeriques = df.select_dtypes(include=['float64', 'int64']).columns
        
        # Filtre sur une colonne numérique
        colonne_selection = st.sidebar.selectbox(
            "Sélectionner une colonne pour filtrer", 
            colonnes_numeriques
        )
        
        # Slider de filtrage
        min_val = float(df[colonne_selection].min())
        max_val = float(df[colonne_selection].max())
        
        valeur_filtre = st.sidebar.slider(
            f"Filtrer par {colonne_selection}", 
            min_val, 
            max_val, 
            (min_val, max_val)
        )
        
        # Appliquer le filtre
        df_filtré = df[
            (df[colonne_selection] >= valeur_filtre[0]) & 
            (df[colonne_selection] <= valeur_filtre[1])
        ]
        
        st.subheader(f"Données filtrées par {colonne_selection}")
        st.dataframe(df_filtré)
        
    else:
        st.error("Impossible de charger les données")

if __name__ == "__main__":
    main()