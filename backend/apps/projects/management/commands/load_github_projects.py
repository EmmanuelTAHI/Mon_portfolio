"""
Commande Django pour charger les projets depuis les dépôts GitHub.
Usage: python manage.py load_github_projects
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.projects.models import Project


class Command(BaseCommand):
  help = "Charge les projets depuis les dépôts GitHub spécifiés"

  def handle(self, *args, **options):
      projects_data = [
          {
              "title": "E-commerce Application",
              "github_url": "https://github.com/EmmanuelTAHI/E-commerce-test/tree/master",
              "description": "Application e-commerce complète développée avec Django et TailwindCSS. Cette application web moderne offre une expérience utilisateur fluide pour la gestion de produits, panier d'achat, authentification utilisateur, et transactions en ligne. Interface responsive avec design moderne et sécurisé.",
              "short_description": "Application e-commerce Django avec TailwindCSS et authentification",
              "technologies": "Django, Python, TailwindCSS, HTML, CSS, JavaScript, PostgreSQL, REST API",
              "category": "web",
          },
          {
              "title": "Savoirs - Knowledge Management System",
              "github_url": "https://github.com/EmmanuelTAHI/projet_agile_2",
              "description": "Système de gestion des connaissances (Knowledge Management System) appelé 'Savoirs', développé dans le cadre d'un projet agile. Permet l'organisation, le partage, la recherche et la catégorisation de connaissances au sein d'une organisation. Interface intuitive avec système de tags et de recherche avancée.",
              "short_description": "Système de gestion des connaissances développé en méthode agile (Savoirs)",
              "technologies": "Python, Django, PostgreSQL, HTML, CSS, JavaScript, Agile Methodology",
              "category": "web",
          },
          {
              "title": "CANTINE-HEG - Mobile Canteen Management",
              "github_url": "https://github.com/EmmanuelTAHI/CANTINE-HEG",
              "description": "Application mobile native pour la gestion de cantine scolaire développée avec Flutter. Permet aux étudiants de consulter les menus quotidiens, réserver des repas à l'avance, gérer leurs commandes, et suivre leurs dépenses. Interface utilisateur intuitive avec notifications push et système de paiement intégré.",
              "short_description": "Application mobile Flutter de gestion de cantine scolaire",
              "technologies": "Flutter, Dart, Mobile Development, REST API, Firebase, State Management",
              "category": "mobile",
          },
          {
              "title": "DJANGO_BOOKS - E-commerce de Livres",
              "github_url": "https://github.com/EmmanuelTAHI/DJANGO_BOOKS",
              "description": "Plateforme e-commerce complète spécialisée dans la vente de livres, développée avec Django. Inclut un système de blog intégré pour les critiques et actualités littéraires, gestion complète du catalogue avec recherche et filtres, panier d'achat, système de paiement sécurisé, et espace administrateur pour la gestion des stocks et commandes.",
              "short_description": "Plateforme e-commerce de livres avec système de blog intégré",
              "technologies": "Django, Python, PostgreSQL, HTML, CSS, JavaScript, REST API, Authentication",
              "category": "web",
          },
          {
              "title": "CI-VOTE-MOBILE - Mobile Voting Application",
              "github_url": "https://github.com/EmmanuelTAHI/CI-VOTE-MOBILE/tree/master",
              "description": "Application mobile sécurisée de vote en ligne développée avec Flutter, utilisée pour les élections en ligne. Assure la sécurité des données avec chiffrement, authentification multi-facteurs, transparence du processus électoral avec traçabilité, et accessibilité via une interface mobile intuitive. Système de vérification et audit intégré.",
              "short_description": "Application mobile sécurisée de vote en ligne pour élections",
              "technologies": "Flutter, Dart, Mobile Development, Security, REST API, Authentication, Encryption, JWT",
              "category": "mobile",
          },
      ]

      created_count = 0
      updated_count = 0

      for project_data in projects_data:
          slug = slugify(project_data["title"])
          project, created = Project.objects.update_or_create(
              slug=slug,
              defaults={
                  "title": project_data["title"],
                  "github_url": project_data["github_url"],
                  "description": project_data["description"],
                  "short_description": project_data["short_description"],
                  "technologies": project_data["technologies"],
                  "category": project_data["category"],
              },
          )

          if created:
              created_count += 1
              self.stdout.write(
                  self.style.SUCCESS(f'[OK] Projet cree: {project.title}')
              )
          else:
              updated_count += 1
              self.stdout.write(
                  self.style.WARNING(f'[UPDATE] Projet mis a jour: {project.title}')
              )

      self.stdout.write(
          self.style.SUCCESS(
              f'\n[TERMINE] {created_count} crees, {updated_count} mis a jour'
          )
      )
