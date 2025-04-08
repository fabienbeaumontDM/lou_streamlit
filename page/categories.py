import streamlit as st
import streamlit_antd_components as sac
import altair as alt
import streamlit_shadcn_ui as ui
from st_aggrid import AgGrid, GridOptionsBuilder
from data.load_dataset import load_joueurs_par_categorie_evol


# --- SETUP PAGE ---
def page_categories():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-bookmark-star"></i> Catégories et saisons</h1>
    """, unsafe_allow_html=True)
    
    #--- Chargement des données ---
    # Charger les datasets
    df_histo_categorie = load_joueurs_par_categorie_evol()

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
    col1, col2 = st.columns([40, 60])  # Créer deux colonnes avec des proportions différentes

    with col1:
         # Titre pour la colonne 1
        st.subheader("Catégorie")
        # Sélecteur pour les catégories
        selected_categorie = ui.tabs(options=categorie, default_value=categorie[0], key="categorie_tabs")

    with col2:
        # Titre pour la colonne 2
        st.subheader("Saison")
        # Sélecteur pour les saisons
        selected_saison = ui.tabs(options=saison, default_value=saison[0], key="saison_tabs")

    # Initialiser le DataFrame filtré avec toutes les données
    filtered_data = df_histo_categorie

    # Appliquer le filtre pour les saisons
    if selected_saison != "Toutes":
        filtered_data = filtered_data[filtered_data["LB_SAISON"] == selected_saison]

    # Appliquer le filtre pour les catégories
    if selected_categorie != "Toutes":
        filtered_data = filtered_data[filtered_data["LB_CATEGORIE"] == selected_categorie]

    # Afficher les données filtrées
    with st.expander("Afficher les données filtrées", expanded=False):
        AgGrid(
            filtered_data.head(50),
            gridOptions=GridOptionsBuilder.from_dataframe(filtered_data).build(),
        )

    # Histogramme par saison et catégories
    with st.container():
        st.subheader("Historique du nombre de joueurs par catégorie et par saison")
        filtered_data = filtered_data[filtered_data["CD_CATEGORIE"] != 0]  # Exclure les totaux
        filtered_data = filtered_data[filtered_data["CD_SAISON"] != 0]  # Exclure les totaux
        chart = alt.Chart(filtered_data).mark_bar().encode(
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