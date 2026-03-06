from django.db import models


class Skill(models.Model):
  CATEGORY_CHOICES = [
      ("pentesting", "Penetration Testing"),
      ("networking", "Networking"),
      ("programming", "Programming"),
      ("web", "Web"),
      ("security", "Security"),
      ("other", "Other"),
  ]

  name = models.CharField(max_length=120)
  category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
  level = models.PositiveIntegerField(
      default=70,
      help_text="Niveau de 0 à 100 pour l’animation des barres",
  )
  icon = models.CharField(
      max_length=60,
      blank=True,
      help_text="Nom d’icône (par ex. Heroicons / Lucide côté frontend)",
  )
  description = models.CharField(max_length=255, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
      ordering = ["category", "-level"]

  def __str__(self) -> str:
      return f"{self.name} ({self.category})"
