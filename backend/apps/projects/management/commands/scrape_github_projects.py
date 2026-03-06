"""
Script pour scraper les dépôts GitHub et extraire les informations réelles.
Usage: python manage.py scrape_github_projects
"""

import requests
import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.projects.models import Project


class Command(BaseCommand):
  help = "Scrape les dépôts GitHub pour extraire les technologies et descriptions réelles"

  def handle(self, *args, **options):
      # URLs des dépôts GitHub
      repos = [
          {
              "url": "https://github.com/EmmanuelTAHI/E-commerce-test",
              "branch": "master",
              "title": "E-commerce Application",
              "category": "web",
          },
          {
              "url": "https://github.com/EmmanuelTAHI/projet_agile_2",
              "branch": None,
              "title": "Savoirs - Knowledge Management System",
              "category": "web",
          },
          {
              "url": "https://github.com/EmmanuelTAHI/CANTINE-HEG",
              "branch": None,
              "title": "CANTINE-HEG - Mobile Canteen Management",
              "category": "mobile",
          },
          {
              "url": "https://github.com/EmmanuelTAHI/DJANGO_BOOKS",
              "branch": None,
              "title": "DJANGO_BOOKS - E-commerce de Livres",
              "category": "web",
          },
          {
              "url": "https://github.com/EmmanuelTAHI/CI-VOTE-MOBILE",
              "branch": "master",
              "title": "CI-VOTE-MOBILE - Mobile Voting Application",
              "category": "mobile",
          },
      ]

      created_count = 0
      updated_count = 0

      for repo_info in repos:
          try:
              # Construire l'URL de l'API GitHub
              repo_path = repo_info["url"].replace("https://github.com/", "")
              api_url = f"https://api.github.com/repos/{repo_path}"
              
              self.stdout.write(f"\n📦 Analyse de {repo_info['title']}...")
              
              # Récupérer les informations du dépôt via l'API GitHub
              response = requests.get(api_url, timeout=10)
              
              if response.status_code == 200:
                  repo_data = response.json()
                  
                  # Extraire les informations
                  description = repo_data.get("description", "")
                  default_branch = repo_data.get("default_branch", "main")
                  
                  # Récupérer le README pour détecter les technologies
                  readme_url = f"https://api.github.com/repos/{repo_path}/readme"
                  readme_response = requests.get(readme_url, timeout=10)
                  
                  technologies = self.detect_technologies(repo_data, readme_response)
                  
                  # Générer une description professionnelle
                  full_description = self.generate_description(
                      repo_info["title"],
                      description,
                      repo_data.get("language", ""),
                      technologies,
                      repo_info["category"]
                  )
                  
                  short_description = description if description else self.generate_short_description(
                      repo_info["title"],
                      repo_info["category"],
                      technologies
                  )
                  
                  # Construire l'URL GitHub complète
                  github_url = repo_info["url"]
                  if repo_info["branch"]:
                      github_url = f"{repo_info['url']}/tree/{repo_info['branch']}"
                  
                  slug = slugify(repo_info["title"])
                  
                  project, created = Project.objects.update_or_create(
                      slug=slug,
                      defaults={
                          "title": repo_info["title"],
                          "github_url": github_url,
                          "description": full_description,
                          "short_description": short_description,
                          "technologies": ", ".join(technologies) if technologies else "Python, Django",
                          "category": repo_info["category"],
                      },
                  )
                  
                  if created:
                      created_count += 1
                      self.stdout.write(
                          self.style.SUCCESS(f'  ✓ Projet créé: {project.title}')
                      )
                  else:
                      updated_count += 1
                      self.stdout.write(
                          self.style.WARNING(f'  ↻ Projet mis à jour: {project.title}')
                      )
                  
                  self.stdout.write(f"  📋 Technologies détectées: {', '.join(technologies) if technologies else 'Non détectées'}")
                  
              else:
                  self.stdout.write(
                      self.style.ERROR(f"  ✗ Erreur lors de la récupération: {response.status_code}")
                  )
                  # Créer quand même avec les données de base
                  self.create_fallback_project(repo_info)
                  
          except Exception as e:
              self.stdout.write(
                  self.style.ERROR(f"  ✗ Erreur pour {repo_info['title']}: {str(e)}")
              )
              # Créer quand même avec les données de base
              self.create_fallback_project(repo_info)

      self.stdout.write(
          self.style.SUCCESS(
              f'\n✅ Terminé: {created_count} créés, {updated_count} mis à jour'
          )
      )

  def detect_technologies(self, repo_data, readme_response):
      """Détecte les technologies utilisées dans le projet"""
      technologies = set()
      
      # Langage principal
      language = repo_data.get("language", "")
      if language:
          technologies.add(language)
      
      # Analyser le README si disponible
      if readme_response.status_code == 200:
          readme_content = readme_response.json().get("content", "")
          if readme_content:
              import base64
              try:
                  readme_text = base64.b64decode(readme_content).decode('utf-8')
                  
                  # Détecter les technologies communes
                  tech_patterns = {
                      "Django": ["django", "Django"],
                      "Python": ["python", "Python", "pip install"],
                      "Flutter": ["flutter", "Flutter", "pubspec.yaml"],
                      "Dart": ["dart", "Dart"],
                      "React": ["react", "React", "reactjs"],
                      "Angular": ["angular", "Angular"],
                      "Vue": ["vue", "Vue.js"],
                      "Node.js": ["node", "Node.js", "npm"],
                      "Express": ["express", "Express"],
                      "PostgreSQL": ["postgresql", "PostgreSQL", "psycopg2"],
                      "MySQL": ["mysql", "MySQL"],
                      "MongoDB": ["mongodb", "MongoDB"],
                      "TailwindCSS": ["tailwind", "TailwindCSS", "tailwindcss"],
                      "Bootstrap": ["bootstrap", "Bootstrap"],
                      "JavaScript": ["javascript", "JavaScript", "js"],
                      "TypeScript": ["typescript", "TypeScript", "ts"],
                      "HTML": ["html", "HTML"],
                      "CSS": ["css", "CSS"],
                      "REST API": ["rest", "REST", "api"],
                      "Docker": ["docker", "Docker", "Dockerfile"],
                  }
                  
                  for tech, patterns in tech_patterns.items():
                      if any(pattern in readme_text for pattern in patterns):
                          technologies.add(tech)
              except:
                  pass
      
      # Technologies par défaut selon la catégorie
      if not technologies:
          if repo_data.get("language") == "Python":
              technologies.add("Python")
              technologies.add("Django")
          elif repo_data.get("language") == "Dart":
              technologies.add("Dart")
              technologies.add("Flutter")
      
      return sorted(list(technologies))

  def generate_description(self, title, repo_description, language, technologies, category):
      """Génère une description professionnelle"""
      tech_list = ", ".join(technologies) if technologies else "technologies modernes"
      
      descriptions = {
          "web": f"Application web {title.lower()} développée avec {tech_list}. {repo_description if repo_description else 'Application web moderne offrant une expérience utilisateur fluide et des fonctionnalités avancées.'}",
          "mobile": f"Application mobile {title.lower()} développée avec {tech_list}. {repo_description if repo_description else 'Application mobile native offrant une interface intuitive et des performances optimales.'}",
      }
      
      base_desc = descriptions.get(category, f"Projet {title.lower()} développé avec {tech_list}.")
      
      if "e-commerce" in title.lower() or "commerce" in title.lower():
          base_desc += " Inclut la gestion de produits, panier d'achat, système de paiement et administration complète."
      elif "knowledge" in title.lower() or "savoirs" in title.lower():
          base_desc += " Système permettant l'organisation, le partage et la recherche de connaissances au sein d'une organisation."
      elif "canteen" in title.lower() or "cantine" in title.lower():
          base_desc += " Permet aux utilisateurs de consulter les menus, réserver des repas et gérer leurs commandes."
      elif "book" in title.lower() or "livre" in title.lower():
          base_desc += " Plateforme e-commerce spécialisée avec gestion de catalogue, système de blog intégré et panier d'achat."
      elif "vote" in title.lower() or "voting" in title.lower():
          base_desc += " Application sécurisée pour les élections en ligne, assurant la transparence et l'accessibilité du processus électoral."
      
      return base_desc

  def generate_short_description(self, title, category, technologies):
      """Génère une description courte"""
      tech_list = ", ".join(technologies[:3]) if technologies else "technologies modernes"
      
      if "e-commerce" in title.lower():
          return f"Application e-commerce développée avec {tech_list}"
      elif "knowledge" in title.lower() or "savoirs" in title.lower():
          return f"Système de gestion des connaissances développé avec {tech_list}"
      elif "canteen" in title.lower():
          return f"Application mobile de gestion de cantine développée avec {tech_list}"
      elif "book" in title.lower():
          return f"Plateforme e-commerce de livres avec système de blog"
      elif "vote" in title.lower():
          return f"Application mobile de vote en ligne sécurisée"
      
      return f"Projet {category} développé avec {tech_list}"

  def create_fallback_project(self, repo_info):
      """Crée un projet avec les données de base si le scraping échoue"""
      slug = slugify(repo_info["title"])
      
      fallback_data = {
          "E-commerce Application": {
              "description": "Application e-commerce complète développée avec Django et TailwindCSS. Cette application web moderne offre une expérience utilisateur fluide pour la gestion de produits, panier d'achat, et transactions en ligne.",
              "short_description": "Application e-commerce Django avec TailwindCSS",
              "technologies": "Django, Python, TailwindCSS, HTML, CSS, JavaScript",
          },
          "Savoirs - Knowledge Management System": {
              "description": "Système de gestion des connaissances (Knowledge Management System) développé dans le cadre d'un projet agile. Permet l'organisation, le partage et la recherche de connaissances au sein d'une organisation.",
              "short_description": "Système de gestion des connaissances développé en méthode agile",
              "technologies": "Python, Django, Agile, Web Development",
          },
          "CANTINE-HEG - Mobile Canteen Management": {
              "description": "Application mobile pour la gestion de cantine scolaire. Permet aux étudiants de consulter les menus, réserver des repas, et gérer leurs commandes directement depuis leur smartphone.",
              "short_description": "Application mobile de gestion de cantine scolaire",
              "technologies": "Flutter, Dart, Mobile Development, REST API",
          },
          "DJANGO_BOOKS - E-commerce de Livres": {
              "description": "Site e-commerce spécialisé dans la vente de livres, développé avec Django. Inclut un système de blog intégré, gestion de catalogue, panier d'achat, et système de paiement.",
              "short_description": "Plateforme e-commerce de livres avec système de blog",
              "technologies": "Django, Python, PostgreSQL, HTML, CSS, JavaScript",
          },
          "CI-VOTE-MOBILE - Mobile Voting Application": {
              "description": "Application mobile de vote en ligne utilisée pour les élections. Assure la sécurité, la transparence et l'accessibilité du processus électoral via une interface mobile intuitive.",
              "short_description": "Application mobile de vote en ligne pour élections",
              "technologies": "Flutter, Dart, Mobile Development, Security, REST API, Authentication",
          },
      }
      
      data = fallback_data.get(repo_info["title"], {
          "description": f"Projet {repo_info['category']} développé avec des technologies modernes.",
          "short_description": f"Projet {repo_info['category']}",
          "technologies": "Python, Django",
      })
      
      github_url = repo_info["url"]
      if repo_info["branch"]:
          github_url = f"{repo_info['url']}/tree/{repo_info['branch']}"
      
      Project.objects.update_or_create(
          slug=slug,
          defaults={
              "title": repo_info["title"],
              "github_url": github_url,
              "description": data["description"],
              "short_description": data["short_description"],
              "technologies": data["technologies"],
              "category": repo_info["category"],
          },
      )
