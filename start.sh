#!/bin/bash
set -e

# Aller dans le dossier backend
cd backend || exit 1

# Créer un environnement virtuel si il n'existe pas
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur Django
python manage.py runserver 0.0.0.0:8000
