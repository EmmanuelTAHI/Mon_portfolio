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

## Étape 3 : Import sur Render

1. Attends la fin du déploiement Render (après ton push).
2. **Render** → ton service backend → onglet **Shell** → **Connect**.
3. Dans le Shell :

```bash
cd backend
python manage.py load_production_data --clear
```

`--clear` vide les données actuelles (démo + CTF) puis charge **portfolio_data.json**.  
Sans `--clear`, la commande ne fait que charger la fixture (risque de conflits si les mêmes entités existent déjà).

4. Vérifie : ouvre ton site Vercel, rafraîchis ; tu devrais voir tes projets et expériences, et les images si elles sont bien dans **media/projects/** sur le repo.

---

## En résumé

| Où | Base utilisée | Contenu |
|----|----------------|--------|
| **Local** | Ta base (SQLite/Postgres) | Tes vrais projets + expériences |
| **Vercel + Render** | Base PostgreSQL Render | Avant sync = démo ; après sync = copie de tes données |

Une fois **portfolio_data.json** et les images versionnés et **load_production_data --clear** exécuté sur Render, le front en prod affiche les mêmes données qu’en local (projets, expériences, images).

Pour une prochaine grosse mise à jour : refaire l’export (étape 1), commit/push, puis relancer **load_production_data --clear** dans le Shell Render.
