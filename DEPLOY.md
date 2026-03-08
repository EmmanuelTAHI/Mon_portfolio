# Déploiement Portfolio — Vercel (front + proxy API) + Render (back Django)

Le **frontend** et un **proxy API serverless** sont sur Vercel. Le proxy renvoie `/api/*` vers ton backend Django sur Render.

---

## Déploiement actuel

- **Frontend (Vercel)** : https://frontend-two-mu-14.vercel.app  
  Déjà déployé. Pour que l’API fonctionne (projets, contact, etc.), il reste à :
  1. Déployer le **backend sur Render** (voir ci‑dessous).
  2. Dans **Vercel** → projet *frontend* → **Settings** → **Environment Variables** : ajouter `API_BASE_URL` = l’URL de ton backend Render (ex. `https://portfolio-backend-xxxx.onrender.com`, sans slash final).
  3. Redéployer le frontend (ou attendre le prochain déploiement).

---

## Frontend Angular sur Vercel

### Via le dashboard Vercel (recommandé)

1. Connecte ton repo GitHub sur [vercel.com](https://vercel.com).
2. **Root Directory** : `frontend`
3. **Build Command** : `npm run build`
4. **Output Directory** : `dist/frontend-app/browser` (Angular 17 place l’app dans `browser/`)
5. **Variable d’environnement (obligatoire pour le proxy)** :  
   - Nom : `API_BASE_URL`  
   - Valeur : l’URL de ton backend Render **sans** slash final, ex. `https://mon-portfolio-xyz.onrender.com`  
   Le proxy serverless (`api/proxy.js`) utilise cette variable pour rediriger `/api/*` vers Render.
6. Déploie. Le site sera en `https://ton-projet.vercel.app`, l’API en `https://ton-projet.vercel.app/api`.

### Via Vercel CLI

```bash
# 1. Installer Vercel CLI (une fois)
npm install -g vercel

# 2. Aller dans le dossier frontend
cd frontend

# 3. Builder Angular
npm run build

# 4. Déployer (output = dist/frontend-app/browser)
vercel

# Pour la prod :
vercel --prod
```

Le dossier `frontend/api/` est pris en compte par Vercel (Serverless Functions). Pas besoin de config supplémentaire.

---

## Backend Django sur Render

- **Root Directory** : `backend`
- **Build Command** : `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py load_initial_data && (python manage.py load_production_data --clear || true) && python manage.py collectstatic --noinput`
- **Start Command** : `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120`
- **Variables d’environnement** (Render → Environment) :
  - `DJANGO_SECRET_KEY` : clé secrète (générer une valeur forte)
  - `DJANGO_DEBUG` : `False`
  - `DJANGO_ALLOWED_HOSTS` : `*` ou `.onrender.com`
  - `DATABASE_URL` : fourni automatiquement si une base PostgreSQL est attachée
  - `CSRF_TRUSTED_ORIGINS` : URL du frontend Vercel, ex. `https://ton-projet.vercel.app`
  - Optionnel (email) : `SMTP_USER`, `SMTP_PASSWORD`, `CONTACT_EMAIL`

Un fichier `render.yaml` à la racine du repo permet de définir le service et la base (Blueprint).

---

## Récap

| Composant | Hébergement | URL |
|-----------|-------------|-----|
| Frontend | Vercel | https://ton-projet.vercel.app |
| API (proxy) | Vercel | https://ton-projet.vercel.app/api |
| Backend Django | Render | https://ton-backend.onrender.com |

Le front appelle **/api** (même origine) ; le proxy Vercel envoie tout vers `API_BASE_URL` (Render).

---

## Déploiement pas à pas

### 1. Backend sur Render

1. Va sur [dashboard.render.com](https://dashboard.render.com) → **New** → **Web Service**.
2. Connecte ton dépôt GitHub (celui qui contient ce portfolio).
3. **Root Directory** : `backend`
4. **Build Command** : `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py load_initial_data && (python manage.py load_production_data --clear || true) && python manage.py collectstatic --noinput`
5. **Start Command** : `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
6. Ajoute une **PostgreSQL** (Render → New → PostgreSQL) et copie l’**Internal Database URL** (ou External si tu préfères).
7. Dans le Web Service → **Environment** :
   - `DJANGO_SECRET_KEY` : une clé secrète forte (générateur en ligne ou `openssl rand -base64 48`)
   - `DJANGO_DEBUG` : `False`
   - `DJANGO_ALLOWED_HOSTS` : `*` ou `.onrender.com`
   - `DATABASE_URL` : colle l’URL PostgreSQL
   - `CSRF_TRUSTED_ORIGINS` : laisse vide pour l’instant
8. **Create Web Service**. Une fois le déploiement terminé, note l’URL du backend (ex. `https://portfolio-backend-xxxx.onrender.com`).
9. Dans **Environment**, ajoute ou modifie :  
   `CSRF_TRUSTED_ORIGINS` = `https://ton-projet.vercel.app` (tu mettras la vraie URL Vercel après l’étape 2).

### 2. Frontend sur Vercel

1. Va sur [vercel.com](https://vercel.com) → **Add New** → **Project** → importe le même dépôt.
2. **Root Directory** : `frontend`
3. **Build Command** : `npm run build`
4. **Output Directory** : `dist/frontend-app/browser`
5. **Environment Variables** :
   - `API_BASE_URL` = l’URL du backend Render **sans** slash final (ex. `https://portfolio-backend-xxxx.onrender.com`)
6. **Deploy**. Note l’URL du frontend (ex. `https://portfolio-xxx.vercel.app`).

### 3. Lier frontend et backend

- Sur **Render** : dans le Web Service backend, **Environment** → `CSRF_TRUSTED_ORIGINS` = l’URL Vercel (ex. `https://portfolio-xxx.vercel.app`). Redéploie si besoin.
- Sur **Vercel** : vérifier que `API_BASE_URL` pointe bien vers l’URL Render.

Ensuite ouvre l’URL Vercel : le site doit s’afficher et les appels API (projets, contact, etc.) passent par le proxy vers Render.
