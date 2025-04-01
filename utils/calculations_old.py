import pandas as pd
import numpy as np
from data.data_loader import get_dataset

class DataAnalyzer:
    def __init__(self):
        """
        Initialise l'analyseur de données
        Charge le dataset une seule fois
        """
        self.df = get_dataset()
        
        if self.df is not None:
            self.prepare_data()
    
    def prepare_data(self):
        """
        Méthode pour préparer et transformer les données
        À personnaliser selon vos besoins spécifiques
        """
        # Exemple de transformation
        # Convertir des colonnes, créer des colonnes dérivées, etc.
        pass
    
    def get_categories_distribution(self):
        """
        Récupère la distribution des catégories
        """
        if self.df is None:
            return None
        
        # Exemple avec la colonne 'categorie'
        return self.df['LB_CATEGORIE'].value_counts()
    
    def get_years_distribution(self):
        """
        Récupère la distribution par année
        """
        if self.df is None:
            return None
        
        # Exemple avec une colonne 'annee'
        return self.df['CD_SAISON'].value_counts().sort_index()
    
    def get_clubs_distribution(self):
        """
        Récupère la distribution des clubs
        """
        if self.df is None:
            return None
        
        # Exemple avec la colonne 'club'
        return self.df['LB_NOM_CLUB'].value_counts()
    
    def get_players_distribution(self):
        """
        Récupère la distribution des joueurs
        """
        if self.df is None:
            return None
        
        # Exemple avec la colonne 'joueur'
        return self.df['LB_NOM_COMPLET'].value_counts()
    
    def create_category_chart(self):
        """
        Crée un graphique de distribution des catégories
        """
        distribution = self.get_categories_distribution()
        
        if distribution is None:
            return None
        
        fig = px.pie(
            values=distribution.values, 
            names=distribution.index, 
            title='Distribution des Catégories'
        )
        return fig
    
    def create_years_chart(self):
        """
        Crée un graphique de distribution par année
        """
        distribution = self.get_years_distribution()
        
        if distribution is None:
            return None
        
        fig = px.bar(
            x=distribution.index, 
            y=distribution.values, 
            title='Distribution par Année'
        )
        return fig
    
    # Ajoutez d'autres méthodes de calcul et de visualisation selon vos besoins

# Création d'une instance globale pour être importée
data_analyzer = DataAnalyzer()