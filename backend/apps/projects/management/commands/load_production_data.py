"""
Charge les données réelles du portfolio (export local) sur la base Render.
À lancer une fois sur Render Shell après avoir poussé portfolio_data.json dans backend/fixtures/.

Usage:
  python manage.py load_production_data           # charge fixtures/portfolio_data.json
  python manage.py load_production_data --clear  # vide les données puis charge
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.ctf.models import FlagAttempt, LeaderboardEntry, ChallengeSession
from apps.blog.models import BlogPost
from apps.experience.models import Experience
from apps.projects.models import Project
from apps.skills.models import Skill
from apps.certifications.models import Certification


class Command(BaseCommand):
    help = "Load portfolio_data.json from backend/fixtures/ (your real data for production)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear portfolio + CTF data before loading the fixture",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            FlagAttempt.objects.all().delete()
            LeaderboardEntry.objects.all().delete()
            ChallengeSession.objects.all().delete()
            BlogPost.objects.all().delete()
            Experience.objects.all().delete()
            Project.objects.all().delete()
            Skill.objects.all().delete()
            Certification.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared."))

        try:
            call_command("loaddata", "portfolio_data", verbosity=2, ignorenonexistent=True)
            self.stdout.write(self.style.SUCCESS("Production data loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "File backend/fixtures/portfolio_data.json not found. "
                    "Export from local with: python manage.py dumpdata projects experience skills certifications blog "
                    "--natural-foreign -e contenttypes -e auth.Permission -o backend/fixtures/portfolio_data.json"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Load failed: {e}"))
