import streamlit as st
import streamlit_antd_components as sac
import altair as alt
import streamlit_shadcn_ui as ui
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder
from data.load_dataset import load_joueurs_par_categorie_evol,load_joueurs_club_saison_precedente_detail_nb,load_joueurs_club_saison_suivante_detail_nb


# --- SETUP PAGE ---
def page_categories():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-bookmark-star"></i> Catégories et saisons</h1>
    """, unsafe_allow_html=True)
    
    #--- Chargement des données ---
    # Charger les datasets
    df_histo_categorie = load_joueurs_par_categorie_evol()
    df_provenance_detail = load_joueurs_club_saison_precedente_detail_nb()
    df_destination_detail = load_joueurs_club_saison_suivante_detail_nb()

    # Nb de joueurs par catégorie et par saison
    df_histo_categorie = df_histo_categorie.sort_values(by=["CD_SAISON", "CD_CATEGORIE"], ascending=[True, True])  # Trier par CD_SAISON et CD_CATEGORIE

    if df_histo_categorie.empty:
        st.warning("Aucune donnée disponible.")
        return

    # Obtenir la liste des catégories triées par CD_CATEGORIE
    categorie = df_histo_categorie.sort_values(by="CD_CATEGORIE")["LB_CATEGORIE"].unique().tolist()
    # Obtenir la liste des saisons triées par CD_SAISON
    saison = df_histo_categorie.sort_values(by="CD_SAISON")["LB_SAISON"].unique().tolist()

    # --- Tabs sélection catégories et saison côte à côte ---
    col_filtre1, col_filtre2 = st.columns([40, 60])  # Créer deux colonnes avec des proportions différentes

    with col_filtre1:
         # Titre pour la colonne 1
        st.subheader("Catégorie")
        # Sélecteur pour les catégories
        selected_categorie = ui.tabs(options=categorie, default_value=categorie[0], key="categorie_tabs")

    with col_filtre2:
        # Titre pour la colonne 2
        st.subheader("Saison")
        # Sélecteur pour les saisons
        selected_saison = ui.tabs(options=saison, default_value=saison[0], key="saison_tabs")

    # Provenance des joueurs map
    df_provenance_detail = df_provenance_detail.dropna(subset=["GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE"])  # Supprimer les lignes avec des coordonnées manquantes
    df_provenance_detail = df_provenance_detail[["CD_CATEGORIE", "LB_CATEGORIE","CD_SAISON", "LB_SAISON",
                                                 "LOU_CLUB_SAISON_PRECEDENTE", "GROUPE_CLUB_SAISON_PRECEDENTE", "LB_NOM_CLUB_SAISON_PRECEDENTE",
                                                 "GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE",
                                                 "NB_JOUEUR", "NB_JOUEUR_TOTAL", "PART_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    
    if df_provenance_detail.empty:
        st.warning("Aucune donnée disponible.")
        return

    # Destination des joueurs map
    df_destination_detail = df_destination_detail.dropna(subset=["GEO_LATITUDE_CLUB_SAISON_SUIVANTE", "GEO_LONGITUDE_CLUB_SAISON_SUIVANTE"])  # Supprimer les lignes avec des coordonnées manquantes
    df_destination_detail = df_destination_detail[["CD_CATEGORIE", "LB_CATEGORIE","CD_SAISON", "LB_SAISON",
                                                 "LOU_CLUB_SAISON_SUIVANTE", "GROUPE_CLUB_SAISON_SUIVANTE", "LB_NOM_CLUB_SAISON_SUIVANTE",
                                                 "GEO_LATITUDE_CLUB_SAISON_SUIVANTE", "GEO_LONGITUDE_CLUB_SAISON_SUIVANTE",
                                                 "NB_JOUEUR", "NB_JOUEUR_TOTAL", "PART_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    
    if df_destination_detail.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # Initialiser le DataFrame filtré avec toutes les données
    df_histo_categorie_filtered = df_histo_categorie

    # Appliquer le filtre pour les saisons
    if selected_saison != "Toutes":
        df_histo_categorie_filtered = df_histo_categorie_filtered[df_histo_categorie_filtered["LB_SAISON"] == selected_saison]

    # Appliquer le filtre pour les catégories
    if selected_categorie != "Toutes":
        df_histo_categorie_filtered = df_histo_categorie_filtered[df_histo_categorie_filtered["LB_CATEGORIE"] == selected_categorie]

    # Afficher les données filtrées
    # with st.expander("Afficher les données filtrées", expanded=False):
    #    AgGrid(
    #        df_histo_categorie_filtered.head(50),
    #        gridOptions=GridOptionsBuilder.from_dataframe(df_histo_categorie_filtered).build(),
    #    )

    # Histogramme par saison et catégories
    with st.container():
        st.subheader("Historique du nombre de joueurs par catégorie et par saison")
        df_histo_categorie_filtered = df_histo_categorie_filtered[df_histo_categorie_filtered["CD_CATEGORIE"] != 0]  # Exclure les totaux
        df_histo_categorie_filtered = df_histo_categorie_filtered[df_histo_categorie_filtered["CD_SAISON"] != 0]  # Exclure les totaux
        chart = alt.Chart(df_histo_categorie_filtered).mark_bar().encode(
            x=alt.X("LB_SAISON", title=None,
                    sort=alt.EncodingSortField(field='CD_SAISON', order='ascending')),
            y=alt.Y("NB_JOUEUR", title=None,
                    sort=alt.EncodingSortField(field='CD_CATEGORIE', order='descending')),
            color=alt.Color("LB_CATEGORIE:N",  # Utiliser les noms des catégories pour la légende
                scale=alt.Scale(domain=["18 ans et plus", "Moins de 18 ans", "Moins de 16 ans", "Moins de 15 ans"], 
                                range=["black", "darkred", "red", "lightcoral"]),  # Dégradé de noir à rouge
                title="Catégorie"),
            tooltip=[
                alt.Tooltip("LB_SAISON", title='Saison'),
                alt.Tooltip("LB_CATEGORIE", title='Catégrie'),
                alt.Tooltip("NB_JOUEUR", title='Joueurs'),
                ],
            order=alt.Order("CD_CATEGORIE", sort="ascending")
        )

        # Ajouter les valeurs sur les barres
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=30,  # Décalage vertical pour placer le texte au-dessus des barres
            fill='white'  # Couleur du texte
        ).encode(
            y=alt.Y("NB_JOUEUR", stack="zero"),  # Positionner le texte au centre de la pile
            text=alt.Text("NB_JOUEUR:Q", format='.0f')  # Afficher les valeurs sans décimales
        )

        # Superposer les barres et le texte
        chart = (chart + text).properties(
            width=700,
            height=500
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

    st.divider() # Ligne de séparation

    # Carte de répartition des joueurs par club de provenance et destination
    
    # Coordonnées du LOU Rugby (par exemple : Lyon, France)
    lou_coordinates = [45.753320365, 4.8694300340000005]  # Latitude et longitude du LOU Rugby
    # Coordonnées centrales de la France
    france_coordinates = [46.603354, 1.888334]  # Latitude et longitude de la France
    zoom_level = 6  # Niveau de zoom pour afficher toute la France    
    
    col_map1, col_map2 = st.columns([1, 1])  # Créer deux colonnes de largeur égale

    with col_map1:                       
        # Carte de répartition des joueurs par club de provenance
        st.subheader("Clubs de provenance")

        # Initialiser le DataFrame filtré avec toutes les données
        df_provenance_detail_filtered = df_provenance_detail

        # Appliquer le filtre pour les saisons
        if selected_saison != "Toutes":
            df_provenance_detail_filtered = df_provenance_detail_filtered[df_provenance_detail_filtered["LB_SAISON"] == selected_saison]

        # Appliquer le filtre pour les catégories
        if selected_categorie != "Toutes":
            df_provenance_detail_filtered = df_provenance_detail_filtered[df_provenance_detail_filtered["LB_CATEGORIE"] == selected_categorie]

        # Afficher les données filtrées
        # with st.expander("Afficher les données filtrées", expanded=False):
        #    AgGrid(
        #        df_provenance_detail_filtered.head(50),
        #        gridOptions=GridOptionsBuilder.from_dataframe(df_provenance_detail_filtered).build(),
        #    )
    
        # Grouper par club de provenance et sommer les joueurs
        df_provenance_detail_filtered = df_provenance_detail_filtered.groupby("LB_NOM_CLUB_SAISON_PRECEDENTE", as_index=False).agg({
            "NB_JOUEUR": "sum",
            "NB_JOUEUR_TOTAL": "sum",
            "GEO_LATITUDE_CLUB_SAISON_PRECEDENTE": "first",  # Garder la première latitude
            "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE": "first",  # Garder la première longitude
            "GROUPE_CLUB_SAISON_PRECEDENTE": "first",  # Garder le premier groupe
            "CD_CATEGORIE": "first",  # Garder la première catégorie
            "LB_CATEGORIE": "first",  # Garder le premier label de catégorie
            "CD_SAISON": "first",  # Garder la première saison
            "LB_SAISON": "first"  # Garder le premier label de saison
        })
            
        # Extraire les informations pour le LOU
        lou_data = df_provenance_detail_filtered[df_provenance_detail_filtered["GROUPE_CLUB_SAISON_PRECEDENTE"] == "LOU"]
        lou_nb_joueurs = lou_data["NB_JOUEUR"].sum() if not lou_data.empty else 0
        df_points_rouges = df_provenance_detail_filtered[df_provenance_detail_filtered["GROUPE_CLUB_SAISON_PRECEDENTE"] != "LOU"]

        # Créer une carte centrée sur la France
        m_provenance = folium.Map(location=france_coordinates, zoom_start=zoom_level, control_scale=True)

        # Ajouter un point noir fixe pour le LOU
        folium.Marker(
            location=lou_coordinates,
            icon=folium.Icon(color="black", icon="info-sign"),
            tooltip=folium.Tooltip(f"LOU: {lou_nb_joueurs} joueurs")
        ).add_to(m_provenance)

        # Ajouter des points rouges pour chaque club de provenance
        for _, row in df_points_rouges.iterrows():
            latitude = row.get("GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", None)
            longitude = row.get("GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE", None)
            nb_joueurs = row["NB_JOUEUR"]
            club = row["LB_NOM_CLUB_SAISON_PRECEDENTE"]

            if latitude and longitude:
                folium.Marker(
                    location=[latitude, longitude],
                    icon=folium.Icon(color="red", icon="info-sign"),
                    tooltip=folium.Tooltip(f"{club}: {nb_joueurs} joueurs")
                ).add_to(m_provenance)

        # Afficher la carte dans Streamlit
        st_folium(m_provenance, use_container_width=True, height=700)

    with col_map2:
        # Carte de répartition des joueurs par club de destination
        st.subheader("Clubs de destination")

        # Initialiser le DataFrame filtré avec toutes les données
        df_destination_detail_filtered = df_destination_detail

        # Appliquer le filtre pour les saisons
        if selected_saison != "Toutes":
            df_destination_detail_filtered = df_destination_detail_filtered[df_destination_detail_filtered["LB_SAISON"] == selected_saison]

        # Appliquer le filtre pour les catégories
        if selected_categorie != "Toutes":
            df_destination_detail_filtered = df_destination_detail_filtered[df_destination_detail_filtered["LB_CATEGORIE"] == selected_categorie]

        # Afficher les données filtrées
        # with st.expander("Afficher les données filtrées", expanded=False):
        #    AgGrid(
        #        df_destination_detail_filtered.head(50),
        #        gridOptions=GridOptionsBuilder.from_dataframe(df_destination_detail_filtered).build(),
        #    )
    
        # Grouper par club de destination et sommer les joueurs
        df_destination_detail_filtered = df_destination_detail_filtered.groupby("LB_NOM_CLUB_SAISON_SUIVANTE", as_index=False).agg({
            "NB_JOUEUR": "sum",
            "NB_JOUEUR_TOTAL": "sum",
            "GEO_LATITUDE_CLUB_SAISON_SUIVANTE": "first",  # Garder la première latitude
            "GEO_LONGITUDE_CLUB_SAISON_SUIVANTE": "first",  # Garder la première longitude
            "GROUPE_CLUB_SAISON_SUIVANTE": "first",  # Garder le premier groupe
            "CD_CATEGORIE": "first",  # Garder la première catégorie
            "LB_CATEGORIE": "first",  # Garder le premier label de catégorie
            "CD_SAISON": "first",  # Garder la première saison
            "LB_SAISON": "first"  # Garder le premier label de saison
        })
            
        # Extraire les informations pour le LOU
        lou_data_destination = df_destination_detail_filtered[df_destination_detail_filtered["GROUPE_CLUB_SAISON_SUIVANTE"] == "LOU"]
        lou_nb_joueurs_destination = lou_data_destination["NB_JOUEUR"].sum() if not lou_data_destination.empty else 0
        df_points_rouges_destination = df_destination_detail_filtered[df_destination_detail_filtered["GROUPE_CLUB_SAISON_SUIVANTE"] != "LOU"]

        # Créer une carte centrée sur la France
        m_destination = folium.Map(location=france_coordinates, zoom_start=zoom_level, control_scale=True)

        # Ajouter un point noir fixe pour le LOU
        folium.Marker(
            location=lou_coordinates,
            icon=folium.Icon(color="black", icon="info-sign"),
            tooltip=folium.Tooltip(f"LOU: {lou_nb_joueurs_destination} joueurs")
        ).add_to(m_destination)

        # Ajouter des points rouges pour chaque club de destination
        for _, row in df_points_rouges_destination.iterrows():
            latitude = row.get("GEO_LATITUDE_CLUB_SAISON_SUIVANTE", None)
            longitude = row.get("GEO_LONGITUDE_CLUB_SAISON_SUIVANTE", None)
            nb_joueurs = row["NB_JOUEUR"]
            club = row["LB_NOM_CLUB_SAISON_SUIVANTE"]

            if latitude and longitude:
                folium.Marker(
                    location=[latitude, longitude],
                    icon=folium.Icon(color="red", icon="info-sign"),
                    tooltip=folium.Tooltip(f"{club}: {nb_joueurs} joueurs")
                ).add_to(m_destination)

        # Afficher la carte dans Streamlit
        st_folium(m_destination, use_container_width=True, height=700)

    st.divider()  # Ligne de séparation