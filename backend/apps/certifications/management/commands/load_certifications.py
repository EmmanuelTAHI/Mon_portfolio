"""
Commande Django pour charger les certifications.
Usage: python manage.py load_certifications
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from apps.certifications.models import Certification


class Command(BaseCommand):
  help = "Charge les certifications dans la base de données"

  def handle(self, *args, **options):
      certifications_data = [
          {
              "title": "Cisco Network Technician Career Path",
              "issuer": "Cisco Networking Academy",
              "description": "Parcours de certification technique en réseaux Cisco couvrant les fondamentaux du networking, la configuration de routeurs et commutateurs, et la résolution de problèmes réseau.",
              "credential_url": "https://www.netacad.com/certificates/?issuanceId=6d0ba4f5-7c9a-4fe9-bcc1-df7199c1ee6f",
              "status": "completed",
              "date": date(2024, 1, 15),  # Date approximative, à ajuster selon la date réelle
          },
          {
              "title": "Certified Associate Penetration Tester (CAPT)",
              "issuer": "Hackviser",
              "description": "Certification en cours d'obtention en penetration testing. Couvre les techniques d'évaluation de sécurité, exploitation de vulnérabilités, et reporting éthique.",
              "credential_url": "",
              "status": "in-progress",
              "date": date.today(),  # Date de début
          },
      ]

      created_count = 0
      updated_count = 0

      for cert_data in certifications_data:
          cert, created = Certification.objects.update_or_create(
              title=cert_data["title"],
              issuer=cert_data["issuer"],
              defaults={
                  "description": cert_data["description"],
                  "credential_url": cert_data["credential_url"],
                  "status": cert_data["status"],
                  "date": cert_data["date"],
              },
          )

          if created:
              created_count += 1
              self.stdout.write(
                  self.style.SUCCESS(f'[OK] Certification creee: {cert.title} - {cert.issuer}')
              )
          else:
              updated_count += 1
              self.stdout.write(
                  self.style.WARNING(f'[UPDATE] Certification mise a jour: {cert.title} - {cert.issuer}')
              )

      self.stdout.write(
          self.style.SUCCESS(
              f'\n[TERMINE] {created_count} creees, {updated_count} mises a jour'
          )
      )
