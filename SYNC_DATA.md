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

**Sans ces images dans le repo, le site en prod affiche le placeholder « Photo du projet ».** Les images sont versionnées dans **backend/media/projects/** (le dossier `media` n’est plus dans le .gitignore).

Les images doivent être dans **backend/media/projects/** avec **exactement** ces noms (tels que dans ta fixture) :

| Fichier attendu        | Projet              |
|------------------------|---------------------|
| `e_commerce.png`       | E-commerce Application |
| `savoirs.png`          | Savoirs             |
| `heg.png`              | CANTINE-HEG         |
| `django_books.png`     | DJANGO_BOOKS        |
| `ci_vote.png`          | CI-VOTE-MOBILE      |

À faire :

1. Crée le dossier `backend/media/projects/` s’il n’existe pas.
2. Copie tes visuels dans ce dossier en les renommant comme ci‑dessus (ou ajuste la fixture si tu gardes d’autres noms).
3. Commit et push (par ex. `git add .` puis `git commit` et `git push`).

Après le redéploiement sur Render, les URLs `https://portfolio-backend-xxx.onrender.com/media/projects/xxx.png` serviront bien les images.

---

## Étape 3 : Import sur Render (sans Shell)

Comme le Shell Render est une option payante, **l’import se fait automatiquement au build** :

1. Après avoir poussé **portfolio_data.json** et les images (**backend/media/projects/**), Render redéploie.
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
