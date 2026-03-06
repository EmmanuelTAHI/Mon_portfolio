## Portfolio Cybersecurity – Emmanuel TAHI

Portfolio full‑stack pour présenter ton profil de **Cybersecurity Student / Pentester**, avec :
- **Frontend** : Angular 17 + TailwindCSS + DaisyUI (thème terminal “cyberpunk”)
- **Backend** : Django 6 / Django REST Framework (API pour projets, skills, expériences, blog, contact)

---

## Aperçu

- **Hero section** façon terminal : pseudo‑commande `cat ~/intro.txt`, texte tapé, bouton *Download CV*.
- **Photo** dans un cercle blanc entouré d’un **anneau néon vert animé**.
- Sections : **About, Skills, Projects, Experience, Certifications, Contact**, plus un **challenge CTF** intégré.
- **Formulaire de contact** connecté au backend (envoi d’e‑mails configurable).
- API documentée via **Swagger / OpenAPI**.

Pour plus de détails de déploiement avancé, voir `DEPLOYMENT.md`.

---

## Structure du projet

- `backend/` – API Django (REST, emails, données du portfolio)
- `frontend/` – SPA Angular (UI, animations, intégration API)
- `docs/` – Documentation supplémentaire
- `DEPLOYMENT.md` – Guide déploiement complet (prod, Nginx, etc.)

---

## Prérequis

- **Backend**
  - Python **3.10+**
  - (Optionnel) PostgreSQL 14+ si tu ne veux pas utiliser SQLite
- **Frontend**
  - Node.js **18+**
  - npm **9+**

---

## Installation rapide

### 1. Cloner le dépôt

```bash
git clone <URL_DU_REPO>
cd PORTFOLIO
```

### 2. Backend – Django

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Créer un fichier `.env` dans `backend/` (voir aussi `DEPLOYMENT.md`) :

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Optionnel : PostgreSQL (sinon SQLite par défaut)
DB_ENGINE=postgres
DB_NAME=portfolio
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_HOST=localhost
DB_PORT=5432

# Emails pour le formulaire de contact
SMTP_USER=ton_compte_smtp
SMTP_PASSWORD=motdepasse_application
CONTACT_EMAIL=ton_email_de_reception
```

Initialiser la base :

```bash
cd backend
python manage.py migrate
python manage.py load_initial_data  # insère skills, projets, expériences, blog…
```

Lancer le serveur Django :

```bash
python manage.py runserver
# http://localhost:8000/
# Docs API : http://localhost:8000/api/docs/
```

### 3. Frontend – Angular

Dans un autre terminal :

```bash
cd frontend
npm install
npm start
```

L’UI est disponible sur `http://localhost:4200` et communique avec le backend via le proxy `/api` → `http://localhost:8000`.

---

## Scripts utiles

### Backend

- `python manage.py migrate` – appliquer les migrations
- `python manage.py load_initial_data` – insérer les données de démo
- `python manage.py createsuperuser` – créer un admin Django
- `python manage.py runserver` – lancer le serveur de dev

### Frontend

- `npm start` – `ng serve` pour le développement
- `npm run build` – build de production dans `frontend/dist/frontend-app/`
- `npm test` – lancer les tests Angular (Karma / Jasmine)

---

## Build & déploiement

### Build de production

```bash
# Frontend
cd frontend
npm run build   # dist/frontend-app/

# Backend
cd ../backend
python manage.py collectstatic  # si tu sers aussi les assets Django
```

En production typique :

- Nginx ou autre serveur web sert `frontend/dist/frontend-app/` en statique.
- Les chemins `/api/` (et `/admin/`) sont proxyfiés vers le process Django (Gunicorn, uvicorn, etc.).
- L’API conserve `API_BASE = '/api'` côté frontend pour être agnostique du domaine.

Des exemples plus détaillés (Nginx, Gunicorn…) sont décrits dans `DEPLOYMENT.md`.

---

## Fonctionnalités principales

- **Hero terminal animé** : texte tapé ligne par ligne, curseur clignotant.
- **Photo circulaire** avec **anneaux verts animés** (effet radar / scanner).
- **Timeline d’expérience**, cartes de projets, liste de skills (tech & security).
- **Section CTF / Challenge** avec intégration au backend pour suivre les sessions.
- **Formulaire de contact sécurisé** :
  - validation côté frontend et backend
  - envoi d’e‑mail configurable via `.env`
- **API REST** documentée (`/api/docs/`, `/api/schema/`).

---

## Contribution / personnalisation

- Met à jour ton **CV** dans `frontend/src/assets/pdf/CV Emmanuel TAHI.pdf`.
- Remplace la **photo** dans `frontend/src/assets/images/Mon_image.png`.
- Adapte le texte de l’hero (`HeroComponent`) et les données initiales (`load_initial_data`) selon ton profil.

---

## Licence

Projet personnel de portfolio – utilisation libre pour ton usage propre, à adapter/cloner pour d’autres portefeuilles si tu le souhaites.

