# Diagnostic Render (selon [Troubleshooting Deploys](https://render.com/docs/troubleshooting-deploys))

## 1. Vérifier les logs

- **Build qui échoue** : Dashboard → ton service → **Events** → cliquer sur le déploiement en erreur → logs.
- **App qui crash en runtime** : onglet **Logs** du service, chercher `error` dans l’explorer.

## 2. Versions et configuration (alignées avec Render)

| Élément | Statut | Détail |
|--------|--------|--------|
| **Runtime** | OK | `python` (Web Service). |
| **PYTHON_VERSION** | OK | `3.12.4` (majeur.minor.patch requis par Render). |
| **rootDir** | OK | `backend` → build/start exécutés depuis le bon dossier. |
| **Build command** | OK | `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py load_initial_data && python manage.py collectstatic --noinput`. Correspond au build local. |
| **Start command** | OK | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` → bind sur `0.0.0.0` et port Render (doc: [Port binding](https://render.com/docs/troubleshooting-deploys#502-bad-gateway)). |
| **requirements.txt** | OK | Versions épinglées → même deps qu’en local. |
| **WSGI** | OK | `config.wsgi:application` et fichier `backend/config/wsgi.py` présents. |

## 3. Erreurs courantes déjà traitées

- **Invalid field name(s) for model Project: 'demo_url', 'repo_url'**  
  → Corrigé : `load_initial_data` utilise maintenant `github_url` (aligné avec le modèle `Project`).

- **PYTHON_VERSION must provide major, minor, and patch**  
  → Corrigé : valeur `3.12.4` dans `render.yaml`.

## 4. Variables d’environnement (à définir sur Render)

- **Obligatoires** : `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS`.
- **Optionnel** : SMTP / contact (voir DEPLOY.md).

Si la base est liée via le Blueprint, `DATABASE_URL` peut être injectée automatiquement.

## 5. Recommandation runtime (502 / timeouts)

Sur le plan **free**, le service peut s’endormir ; au réveil la première requête peut dépasser le timeout par défaut de Gunicorn. La doc Render conseille d’augmenter le [timeout Gunicorn](https://docs.gunicorn.org/en/stable/settings.html#timeout).  
→ Start command avec `--timeout 120` (voir modification dans le repo).

## 6. Checklist avant chaque deploy

- [ ] Pas de `repo_url` / `demo_url` dans les commandes ou fixtures (modèle Project).
- [ ] Python en 3 chiffres (ex. `3.12.4`) dans les env vars / Blueprint.
- [ ] Build et Start commands identiques à ceux du `render.yaml` (ou du Dashboard).
- [ ] Logs du dernier deploy consultés en cas d’échec.
