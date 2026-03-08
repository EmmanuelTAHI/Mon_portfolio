# Synchroniser tes vraies données (local → Render)

En local tu vois **tes** projets (CI-VOTE-MOBILE, DJANGO_BOOKS, CANTINE-HEG, etc.) et **tes** expériences. Sur Vercel/Render tu vois les données de démo parce que la base sur Render a été remplie par `load_initial_data` (données génériques).

Il n’y a qu’**un seul backend** (même code), mais **deux bases** :
- **Local** = ta base (SQLite/Postgres) avec tes vraies données
- **Render** = base PostgreSQL remplie par les données de démo

Pour avoir les mêmes infos en prod qu’en local, il faut **exporter** ta base locale et **importer** sur Render (une fois, ou à chaque grosse mise à jour).

---

## Étape 1 : Export en local

Dans le dossier **backend**, avec ton venv activé :

```powershell
cd c:\Users\emman\Downloads\PORTFOLIO\backend
.\venv\Scripts\activate
python manage.py dumpdata projects experience skills certifications blog --natural-foreign -e contenttypes -e auth.Permission -o fixtures/portfolio_data.json
```

Cela crée **backend/fixtures/portfolio_data.json** avec tes projets, expériences, compétences, certifications et billets de blog.

---

## Étape 2 : Images des projets

Les images sont dans **backend/media/projects/** (et éventuellement **media/blog/**).  
Le dossier `media` est ignoré par git ; pour le déployer quand même, utilise `git add -f` :

- Vérifie que **backend/media/projects/** contient bien les images de tes projets (CI-VOTE-MOBILE, etc.).
- Puis, depuis la racine du repo :

```powershell
cd c:\Users\emman\Downloads\PORTFOLIO
git add backend/fixtures/portfolio_data.json
git add -f backend/media/projects/
git add -f backend/media/blog/
git status
git commit -m "Données prod + images projets pour Render"
git push origin main
```

---

## Étape 3 : Import sur Render (sans Shell)

Comme le Shell Render est une option payante, **l’import se fait automatiquement au build** :

1. Après avoir poussé **portfolio_data.json** (et éventuellement les images avec `git add -f backend/media/projects/`), Render redéploie.
2. Pendant le **build**, la commande `load_production_data --clear` est exécutée :
   - si **portfolio_data.json** est présent dans le repo → la base est vidée puis remplie avec tes données ;
   - s’il est absent → le build continue et `load_initial_data` garde les données de démo.
3. Ouvre ton site Vercel : tu devrais voir tes projets et expériences (et les images si **media/projects/** est bien poussé).

Tu n’as rien à lancer à la main sur Render.

---

## En résumé

| Où | Base utilisée | Contenu |
|----|----------------|--------|
| **Local** | Ta base (SQLite/Postgres) | Tes vrais projets + expériences |
| **Vercel + Render** | Base PostgreSQL Render | Avant sync = démo ; après sync = copie de tes données |

Une fois **portfolio_data.json** et les images versionnés et **load_production_data --clear** exécuté sur Render, le front en prod affiche les mêmes données qu’en local (projets, expériences, images).

Pour une prochaine grosse mise à jour : refaire l’export (étape 1), commit/push, puis relancer **load_production_data --clear** dans le Shell Render.
