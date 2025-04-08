import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from data.load_dataset import load_joueurs_par_categorie_evol, load_joueurs_club_saison_precedente_nb, load_joueurs_club_saison_precedente_detail_nb

# --- SETUP PAGE ---
def page_accueil():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-house"></i> Accueil</h1>
    """, unsafe_allow_html=True)
    
    st.write("""
    Bienvenue sur l'application du LOU Rugby.
    
    Vous trouverez ci-dessous les principaux indicateurs des équipes pour la saison 2024-2025.
    
    """)

    st.divider()  # Ligne de séparation   
    
    #--- Chargement des données ---

    # Charger les datasets
    df_kpi = load_joueurs_par_categorie_evol()
    df_histo_categorie = load_joueurs_par_categorie_evol()
    df_provenance = load_joueurs_club_saison_precedente_nb()
    df_provenance_detail = load_joueurs_club_saison_precedente_detail_nb()

    # Joueurs par catégorie et évolution
    df_kpi = df_kpi[["CD_SAISON","CD_CATEGORIE", "LB_CATEGORIE", "NB_JOUEUR", "EVOLUTION"]]  # Sélectionner les colonnes pertinentes
    df_kpi = df_kpi[df_kpi["CD_SAISON"] == 5]  # Filtrer pour la saison 2024-2025 (CD_SAISON = 5)
    df_kpi = df_kpi.reset_index(drop=True)  # Réinitialiser l'index

    if df_kpi.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # Nb de joueurs par catégorie et par saison
    df_histo_categorie = df_histo_categorie[["CD_SAISON","LB_SAISON","CD_CATEGORIE", "LB_CATEGORIE", "NB_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_SAISON"] != 0]  # Exclure les totaux
    df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_CATEGORIE"] != 0]  # Exclure les totaux
    df_histo_categorie = df_histo_categorie.sort_values(by=["CD_SAISON", "CD_CATEGORIE"], ascending=[True, True])  # Trier par CD_SAISON et CD_CATEGORIE

    if df_histo_categorie.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # Provenance des joueurs
    df_provenance = df_provenance[df_provenance["CD_SAISON"] == 5]     # Filtrer pour la saison 2024-2025 (CD_SAISON = 5)
    df_provenance = df_provenance[["CD_CATEGORIE", "LB_CATEGORIE", "GROUPE_CLUB_SAISON_PRECEDENTE", "NB_JOUEUR", "NB_JOUEUR_TOTAL", "PART_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    df_provenance['GROUPE_CLUB_SAISON_PRECEDENTE'] = df_provenance['GROUPE_CLUB_SAISON_PRECEDENTE'].fillna('LOU')  # Remplacer les valeurs manquantes par 'LOU'

    if df_provenance.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # Provenance des joueurs map
    df_provenance_detail = df_provenance_detail.dropna(subset=["GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE"])  # Supprimer les lignes avec des coordonnées manquantes
    df_provenance_detail = df_provenance_detail[df_provenance_detail["CD_SAISON"] == 5]     # Filtrer pour la saison 2024-2025 (CD_SAISON = 5)
    df_provenance_detail = df_provenance_detail[df_provenance_detail["CD_CATEGORIE"] != 1]     # Filtrer pour exclure la catégorie "Moins de 15 ans" (CD_CATEGORIE <> 1)
    df_provenance_detail = df_provenance_detail[["CD_CATEGORIE", "LB_CATEGORIE",
                                                 "LOU_CLUB_SAISON_PRECEDENTE", "GROUPE_CLUB_SAISON_PRECEDENTE", "LB_NOM_CLUB_SAISON_PRECEDENTE",
                                                 "GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE",
                                                 "NB_JOUEUR", "NB_JOUEUR_TOTAL", "PART_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    df_provenance_detail = df_provenance_detail.groupby("LB_NOM_CLUB_SAISON_PRECEDENTE", as_index=False).agg({
        "NB_JOUEUR": "sum",
        "NB_JOUEUR_TOTAL": "sum",
        "GEO_LATITUDE_CLUB_SAISON_PRECEDENTE": "first",  # Garder la première latitude
        "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE": "first",  # Garder la première longitude
        "GROUPE_CLUB_SAISON_PRECEDENTE": "first",  # Garder le premier groupe
        "CD_CATEGORIE": "first",  # Garder la première catégorie
        "LB_CATEGORIE": "first"  # Garder le premier label de catégorie
    })
    # Filtrer les données pour exclure le LOU des points rouges
    df_points_rouges = df_provenance_detail[df_provenance_detail["GROUPE_CLUB_SAISON_PRECEDENTE"] != "LOU"]
    
    if df_provenance_detail.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # --- Pages ---

    # Générer des cartes dynamiques avec st.metric
    st.subheader("Nombre de joueurs par catégorie") 
    cols = st.columns(len(df_kpi))  # Crée autant de colonnes que de lignes dans le DataFrame
    for i, row in df_kpi.iterrows():
        with cols[i]:
            # Formater delta en pourcentage sans décimales
            delta_formatted = f"{int(row['EVOLUTION'])}% saison précédente"  # Convertir en entier et ajouter le symbole %
            st.metric(label=row["LB_CATEGORIE"], value=row["NB_JOUEUR"], delta=delta_formatted, border=True)

    # Histogramme par saison et catégories
    with st.container():
        st.subheader("Historique du nombre de joueurs par catégorie")
        col1, col2 = st.columns([2, 1])  # Crée deux colonnes pour l'affichage
        with col1:
            df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_CATEGORIE"] != 0]  # Exclure les totaux
            df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_SAISON"] != 0]  # Exclure les totaux
            chart = alt.Chart(df_histo_categorie).mark_bar().encode(
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

        with col2:
            st.markdown("""
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            Au cours des dernières saisons, le LOU Rugby a connu une évolution à la baisse du nombre de joueurs total.
            
            La chute est particulièrement marquée pour la saison 2024-2025 dans la catégorie **Moins de 15 ans** avec une **chute de 9%**.
            """, unsafe_allow_html=True)

    st.divider()  # Ligne de séparation

    # Répartition des joueurs par club de provenance
    st.subheader("Répartition des joueurs par club de provenance")

    # Trier les catégories
    categories_sorted = df_provenance[['CD_CATEGORIE', 'LB_CATEGORIE']].drop_duplicates().sort_values(by='CD_CATEGORIE')

    charts = []

    for _, row in categories_sorted.iterrows():
        lb_categorie = row['LB_CATEGORIE']
        
        # Filtrer les données
        subset = df_provenance[df_provenance['LB_CATEGORIE'] == lb_categorie].copy()

        if subset.empty:
            continue  # Passer à la suivante si vide

        # Calcul des parts
        subset.loc[:, 'PART_JOUEUR'] = subset['NB_JOUEUR'] / subset['NB_JOUEUR'].sum()

        # Définir une échelle de couleurs
        color_scale = alt.Scale(
            domain=["LOU", "Autre"],
            range=["black", "red"]
        )

        # Création du donut
        chart = alt.Chart(subset).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('PART_JOUEUR:Q', stack=True),
            color=alt.Color('GROUPE_CLUB_SAISON_PRECEDENTE:N', scale=color_scale, title=None),
            tooltip=[
                alt.Tooltip('GROUPE_CLUB_SAISON_PRECEDENTE', title='Club'),
                alt.Tooltip('NB_JOUEUR', title='Joueurs'),
                alt.Tooltip('PART_JOUEUR', title='Part Joueurs', format='.0%')
            ],
            order=alt.Order('NB_JOUEUR', sort='descending')
        ).properties(
            title=f"Répartition des joueurs ({lb_categorie})",
            width=200,
            height=200
        )

        charts.append(chart)  # Maintenant, on ajoute bien !

    # Affichage des graphiques
    if charts:
        cols = st.columns(len(charts))
        for col, chart in zip(cols, charts):
            with col:
                st.altair_chart(chart)
    else:
        st.write("Aucune donnée disponible pour afficher les graphiques.")

    # Carte de répartition des joueurs par club de provenance
    st.subheader("Carte des clubs de provenance")

    # Coordonnées du LOU Rugby (par exemple : Lyon, France)
    lou_coordinates = [45.753320365, 4.8694300340000005]  # Latitude et longitude du LOU Rugby

    # Extraire les informations pour le LOU
    lou_data = df_provenance_detail[df_provenance_detail["GROUPE_CLUB_SAISON_PRECEDENTE"] == "LOU"]
    lou_nb_joueurs = lou_data["NB_JOUEUR"].sum() if not lou_data.empty else 0

    # Créer une carte centrée dynamiquement
    m = folium.Map(location=lou_coordinates, zoom_start=10, control_scale=True)

    # Ajouter un point noir fixe pour le LOU
    folium.Marker(
        location=lou_coordinates,
        icon=folium.Icon(color="black", icon="info-sign"),  # Icône noire avec un symbole "info"
        tooltip=folium.Tooltip(f"LOU: {lou_nb_joueurs} joueurs")  # Tooltip pour le survol
    ).add_to(m)

    # Ajouter des points rouges pour chaque club de provenance
    for _, row in df_points_rouges.iterrows():
        latitude = row.get("GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", None)
        longitude = row.get("GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE", None)
        nb_joueurs = row["NB_JOUEUR"]
        groupe_club = row["GROUPE_CLUB_SAISON_PRECEDENTE"]
        club = row["LB_NOM_CLUB_SAISON_PRECEDENTE"]

        if latitude and longitude:  # Vérifiez que les coordonnées existent
            folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(color="red", icon="info-sign"),  # Icône rouge avec un symbole "info"
                tooltip=folium.Tooltip(f"{club}: {nb_joueurs} joueurs")  # Tooltip pour le survol
            ).add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, use_container_width=True, height=700)

    st.divider()  # Ligne de séparation