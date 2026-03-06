# Déploiement Portfolio — Vercel (front + proxy API) + Render (back Django)

Le **frontend** et un **proxy API serverless** sont sur Vercel. Le proxy renvoie `/api/*` vers ton backend Django sur Render.

---

## Frontend Angular sur Vercel

### Via le dashboard Vercel (recommandé)

1. Connecte ton repo GitHub sur [vercel.com](https://vercel.com).
2. **Root Directory** : `frontend`
3. **Build Command** : `npm run build`
4. **Output Directory** : `dist/frontend-app`
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

# 4. Déployer (Vercel détecte Angular et utilise dist/frontend-app)
vercel

# Pour la prod :
vercel --prod
```

Le dossier `frontend/api/` est pris en compte par Vercel (Serverless Functions). Pas besoin de config supplémentaire.

---

## Backend Django sur Render

- **Root Directory** : `backend`
- **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command** : `gunicorn config.wsgi:application --bind 0.0.0.0:8000`
- Variables d’environnement : voir la liste (DJANGO_SECRET_KEY, DB_*, CSRF_TRUSTED_ORIGINS, etc.) dans Render → Environment.

---

## Récap

| Composant | Hébergement | URL |
|-----------|-------------|-----|
| Frontend | Vercel | https://ton-projet.vercel.app |
| API (proxy) | Vercel | https://ton-projet.vercel.app/api |
| Backend Django | Render | https://ton-backend.onrender.com |

Le front appelle **/api** (même origine) ; le proxy Vercel envoie tout vers `API_BASE_URL` (Render).
