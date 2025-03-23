# lou_streamlit
Repository pour l'application Streamlit du LOU Rugby pour le suivi et l'analyse des joueuses et joueurs des équipes nationales.

Cette application est développée à [Streamlit](https://streamlit.io/). ([documentation](https://docs.streamlit.io/))

## Initialisation du projet

- Cloner le reporsitory Github
- Installer  **uv** ([documentation](https://docs.astral.sh/uv/))
  - ouvrir un terminal
  - se placer dans le répertoire de l'application
  - exécuter la commande *pip install uv*
- Initialiser un projet Python
  - se positionner dans le répertoire de l'application
  - exécuter la commande *uv init*
  - la structure du projet est générée automatiquement
- Créer un environnement virtuel pour le projet
  - se positionner dans le répertoire de l'application
  - exécuter la commande *uv venv --python 3.12*
  - activer l'environement avec la commande *.venv\Scripts\activate*
- Installer les librairies Python *streamlit* et *pandas*
  - se placer dans le répertoire de l'application
  - exécuter la commande *uv pip install streamlit pandas*
  - exécuter la commande *pip freeze > requirements.txt* pour référencer les librairies utilisées dans le projet
- Supprimer manuellement le fichier *hello.py*