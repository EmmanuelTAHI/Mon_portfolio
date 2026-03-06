# Aller dans le dossier backend
cd backend

# Créer l'environnement virtuel si inexistant
if (!(Test-Path -Path "venv")) {
    python -m venv venv
}

# Activer l'environnement virtuel
. .\venv\Scripts\activate

# Installer les dépendances
python -m pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur Django
python manage.py runserver 0.0.0.0:8000