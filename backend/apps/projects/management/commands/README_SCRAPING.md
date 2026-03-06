# Scripts de Chargement des Projets GitHub

## Scripts Disponibles

### 1. `load_github_projects.py` (Recommandé)
Script simple qui charge les projets avec des données pré-définies basées sur l'analyse des dépôts.

**Usage:**
```bash
cd backend
python manage.py load_github_projects
```

**Avantages:**
- Rapide et fiable
- Pas de dépendance externe
- Données optimisées et professionnelles

### 2. `scrape_github_projects.py` (Avancé)
Script qui scrappe réellement les dépôts GitHub via l'API pour extraire les technologies et descriptions.

**Prérequis:**
```bash
pip install requests
```

**Usage:**
```bash
cd backend
python manage.py scrape_github_projects
```

**Fonctionnalités:**
- Détection automatique des technologies via l'API GitHub
- Analyse du README pour identifier les dépendances
- Génération automatique de descriptions professionnelles
- Fallback sur données pré-définies en cas d'erreur

**Note:** L'API GitHub a une limite de 60 requêtes/heure sans authentification. Pour plus de requêtes, configurez un token GitHub dans les variables d'environnement.

## Projets Chargés

1. **E-commerce Application** - Django + TailwindCSS
2. **Savoirs - Knowledge Management System** - Django + PostgreSQL
3. **CANTINE-HEG** - Flutter/Dart (Mobile)
4. **DJANGO_BOOKS** - Django + Blog intégré
5. **CI-VOTE-MOBILE** - Flutter/Dart (Mobile sécurisé)

## Après le Chargement

Les projets seront disponibles via l'API:
- `GET /api/projects/` - Liste tous les projets
- `GET /api/projects/{slug}/` - Détails d'un projet

Et visibles dans la section Projects du portfolio frontend.
