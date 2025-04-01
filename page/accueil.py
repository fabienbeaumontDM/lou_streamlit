import streamlit as st
import altair as alt
import folium
from streamlit_folium import st_folium
from utils.load_dataset import load_joueurs_par_categorie_evol, load_joueurs_club_saison_precedente_nb, load_joueurs_club_saison_precedente_detail_nb

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

    st.markdown("""---""", unsafe_allow_html=True)  # Ligne de séparation    
    
    #--- Chargement des données ---

    # Charger les datasets
    df_kpi = load_joueurs_par_categorie_evol()
    df_histo_categorie = load_joueurs_par_categorie_evol()
    df_provenance = load_joueurs_club_saison_precedente_nb()
    df_provenance_detail = load_joueurs_club_saison_precedente_detail_nb()

    # Joueurs par catégorie et évolution
    df_kpi = df_kpi[["CD_SAISON","CD_CATEGORIE", "LB_CATEGORIE", "NB_JOUEUR", "EVOLUTION"]]  # Sélectionner les colonnes pertinentes
    df_kpi = df_kpi[df_kpi["CD_SAISON"] == 5]  # Filtrer pour la saison 2024-2025 (CD_SAISON = 5)
    df_kpi = df_kpi.sort_values(by="CD_CATEGORIE", ascending=False)  # Trier par CD_CATEGORIE de manière décroissante
    df_kpi = df_kpi.reset_index(drop=True)  # Réinitialiser l'index

    if df_kpi.empty:
        st.warning("Aucune donnée disponible.")
        return
    
    # Nb de joueurs par catégorie et par saison
    df_histo_categorie = df_histo_categorie[["CD_SAISON","LB_SAISON","CD_CATEGORIE", "LB_CATEGORIE", "NB_JOUEUR"]]  # Sélectionner les colonnes pertinentes
    df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_SAISON"] != 99]  # Exclure les totaux
    df_histo_categorie = df_histo_categorie[df_histo_categorie["CD_CATEGORIE"] != 99]  # Exclure les totaux
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
    df_provenance_detail = df_provenance_detail[df_provenance_detail["CD_SAISON"] == 5]     # Filtrer pour la saison 2024-2025 (CD_SAISON = 5)
    df_provenance_detail = df_provenance_detail[df_provenance_detail["CD_CATEGORIE"] != 1]     # Filtrer pour exclure la catégorie "Moins de 15 ans" (CD_CATEGORIE <> 1)
    df_provenance_detail = df_provenance_detail[["CD_CATEGORIE", "LB_CATEGORIE",
                                                 "LOU_CLUB_SAISON_PRECEDENTE", "GROUPE_CLUB_SAISON_PRECEDENTE", "LB_NOM_CLUB_SAISON_PRECEDENTE",
                                                 "GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", "GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE",
                                                 "NB_JOUEUR", "NB_JOUEUR_TOTAL", "PART_JOUEUR"]]  # Sélectionner les colonnes pertinentes

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
            ).properties(
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

    st.markdown("""---""", unsafe_allow_html=True)  # Ligne de séparation 

    # Répartition des joueurs par club de provenance
    st.subheader("Répartition des joueurs par club de provenance")

    categories_sorted = df_provenance[['CD_CATEGORIE', 'LB_CATEGORIE']].drop_duplicates().sort_values(by='CD_CATEGORIE')
    charts = []
    for _, row in categories_sorted.iterrows():
        lb_categorie = row['LB_CATEGORIE']
        subset = df_provenance[df_provenance['LB_CATEGORIE'] == lb_categorie]
        
        # Calcul de la part des joueurs pour chaque groupe
        subset['PART_JOUEUR'] = subset['NB_JOUEUR'] / subset['NB_JOUEUR'].sum()

        # Définir une échelle de couleurs personnalisée
        color_scale = alt.Scale(
            domain=["LOU", "Autre"],  # Les groupes spécifiques
            range=["black", "red"]   # Couleurs correspondantes
        )

        # Création du donut
        chart = alt.Chart(subset).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('PART_JOUEUR:Q', stack=True),
            color=alt.Color('GROUPE_CLUB_SAISON_PRECEDENTE:N', scale=color_scale, title=None),
            tooltip=[
                alt.Tooltip('GROUPE_CLUB_SAISON_PRECEDENTE', title='Club'),
                alt.Tooltip('NB_JOUEUR', title='Joueurs'),
                alt.Tooltip('PART_JOUEUR', title='Part Joueurs', format='.0%')  # Afficher en pourcentage
            ],
            order=alt.Order('NB_JOUEUR', sort='descending')  # Trier par nombre de joueurs pour la légende
        ).properties(
            title=f"Répartition des joueurs ({lb_categorie})",
            width=200,
            height=200
        )

        charts.append(chart)

    # Afficher les donuts dans des colonnes
    cols = st.columns(len(charts))

    for col, chart in zip(cols, charts):
        with col:
            st.altair_chart(chart)

    # Carte de répartition des joueurs par club de provenance
    # Coordonnées du LOU Rugby (par exemple : Lyon, France)
    lou_coordinates = [45.753320365, 4.8694300340000005]  # Latitude et longitude du LOU Rugby

    # Créer une carte centrée sur le LOU
    m = folium.Map(location=lou_coordinates, zoom_start=10)

    # Ajouter des points pour chaque club de provenance
    for _, row in df_provenance.iterrows():
        latitude = row.get("GEO_LATITUDE_CLUB_SAISON_PRECEDENTE", None)
        longitude = row.get("GEO_LONGITUDE_CLUB_SAISON_PRECEDENTE", None)
        nb_joueurs = row["NB_JOUEUR"]
        groupe_club = row["GROUPE_CLUB_SAISON_PRECEDENTE"]
        club = row["LB_NOM_CLUB_SAISON_PRECEDENTE"]

        if latitude and longitude:  # Vérifiez que les coordonnées existent
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=nb_joueurs / 5,  # Ajustez la taille du cercle en fonction du nombre de joueurs
                color="red" if groupe_club == "Autre" else "black",
                fill=True,
                fill_color="red" if groupe_club == "Autre" else "black",
                fill_opacity=0.6,
                popup=f"{club}: {nb_joueurs} joueurs"
            ).add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, width=700, height=500)



