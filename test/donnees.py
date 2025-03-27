import pandas as pd
import numpy as np

# Définir une graine pour la reproductibilité
np.random.seed(42)

# Générer des données de test
n_rows = 100

# Créer un DataFrame avec différents types de colonnes
df = pd.DataFrame({
    'id': range(1, n_rows + 1),
    'categorie': np.random.choice(['A', 'B', 'C'], n_rows),
    'colonne_brute': np.random.normal(100, 15, n_rows),
    'colonne1': np.random.randint(10, 100, n_rows),
    'colonne2': np.random.uniform(0, 10, n_rows),
    'colonne_numerique': np.cumsum(np.random.normal(0, 1, n_rows)),
    'colonne_categorique': np.random.choice(['valeur1', 'valeur2', 'valeur_specifique'], n_rows)
})

# Ajouter quelques valeurs manquantes pour simuler un jeu de données réel
df.loc[np.random.choice(df.index, 10), 'colonne_brute'] = np.nan

# Sauvegarder le fichier CSV
df.to_csv('donnees.csv', index=False)

print(df.head())
print("\nFichier donnees.csv généré avec succès !")

# Vérification des types de colonnes
print("\nTypes de colonnes :")
print(df.dtypes)