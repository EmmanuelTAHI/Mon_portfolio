# Déploiement sur Render

Ce document décrit comment déployer le portfolio (backend Django + frontend Angular) sur [Render](https://render.com) pour que le site soit entièrement fonctionnel dès le premier déploiement.

## Vue d’ensemble

| Service        | Type         | Rôle |
|----------------|-------------|------|
| **portfolio-api** | Web Service | API Django (projets, compétences, expérience, contact, certifications, CTF) |
| **portfolio-frontend** | Static Site | Application Angular compilée |

Le frontend appelle l’API via l’URL du backend. CORS et CSRF sont configurés pour accepter l’origine du frontend.

## 1. Backend (Django)

### Build / Start (render.yaml)

- **Build** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start** : `python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### Variables d’environnement recommandées

| Variable | Description | Exemple |
|----------|-------------|--------|
| `DJANGO_SECRET_KEY` | Clé secrète (générée ou forte) | (générer) |
| `DJANGO_DEBUG` | Désactiver en prod | `False` |
| `DJANGO_ALLOWED_HOSTS` | Hôtes autorisés | `.onrender.com` ou `portfolio-api.onrender.com` |
| `DATABASE_URL` | URL Postgres (fournie si base Render liée) | `postgres://...` |
| `CSRF_TRUSTED_ORIGINS` | Origine du frontend (obligatoire pour formulaire contact) | `https://portfolio-frontend.onrender.com` |
| `CONTACT_EMAIL` | Email qui reçoit les messages du formulaire | `vous@email.com` |
| `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL` | Envoi d’emails (optionnel) | (config Gmail / autre) |

Sans `DATABASE_URL`, le projet utilise SQLite (données perdues à chaque redéploiement sur Render). Pour une base persistante, attacher une base PostgreSQL au service.

## 2. Frontend (Angular)

### Build pour Render

- **Build** : `npm ci && npm run build:render`

`build:render` exécute `scripts/replace-api-url.js` puis `ng build`. Le script injecte l’URL de l’API dans `environment.prod.ts` à partir de la variable d’environnement.

### Variable d’environnement obligatoire

| Variable | Description | Exemple |
|----------|-------------|--------|
| `API_BASE_URL` | URL complète du backend (sans slash final) | `https://portfolio-api.onrender.com` |

À définir dans le dashboard Render pour le service **Static Site** avant le premier build.

### Sortie du build

- **Publish directory** : `dist/frontend-app/browser`

## 3. Endpoints API utilisés par le frontend

| Méthode | Chemin | Usage |
|--------|--------|--------|
| GET | `/api/projects/` | Liste paginée (page, page_size) |
| GET | `/api/projects/:slug/` | Détail d’un projet |
| GET | `/api/skills/` | Liste des compétences |
| GET | `/api/experience/` | Liste des expériences |
| GET | `/api/certifications/` | Liste des certifications |
| POST | `/api/contact/` | Envoi du formulaire de contact |
| POST | `/api/ctf/start/` | Démarrage du challenge CTF |
| POST | `/api/ctf/ubiquiti-login/` | Login simulé Ubiquiti |
| GET | `/api/ctf/download-image/?session_id=...` | Téléchargement image CTF |
| POST | `/api/ctf/submit-final-flag/` | Soumission du flag final |
| GET | `/api/ctf/leaderboard/` | Classement |
| GET | `/api/ctf/check-session/?session_id=...` | Vérification de session |
| GET | `/api/ctf/session-info/?session_id=...` | Infos session (timer) |
| POST | `/api/ctf/abandon-session/` | Abandon de la session |

## 4. Ordre de déploiement

1. Créer et déployer le **backend** (Web Service).
2. Noter l’URL du backend (ex. `https://portfolio-api.onrender.com`).
3. Créer le **frontend** (Static Site) et définir `API_BASE_URL` = URL du backend.
4. Dans le backend, définir `CSRF_TRUSTED_ORIGINS` = URL du frontend (ex. `https://portfolio-frontend.onrender.com`).
5. Redéployer le backend si besoin après avoir mis à jour `CSRF_TRUSTED_ORIGINS`.

## 5. Fichiers utiles

- **render.yaml** : schéma des services (backend + frontend + optionnel DB).
- **frontend/scripts/replace-api-url.js** : injection de `API_BASE_URL` dans le build prod.
- **frontend/src/environments/environment.prod.ts** : `apiBase` utilisé en production (remplacé par le script si `build:render`).

Une fois ces étapes faites, le site est opérationnel : pages d’accueil, projets, détail projet, compétences, expérience, certifications, formulaire de contact et challenge CTF utilisent tous l’API du backend déployé sur Render.
