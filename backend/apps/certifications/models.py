from django.db import models


class Certification(models.Model):
  STATUS_CHOICES = [
      ("completed", "Completed"),
      ("in-progress", "In Progress"),
  ]

  title = models.CharField(max_length=200)
  issuer = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  credential_url = models.URLField(blank=True, help_text="URL du certificat ou de la vérification")
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default="completed",
  )
  date = models.DateField(help_text="Date d'obtention ou de début")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ["-date", "-created_at"]

  def __str__(self) -> str:
      return f"{self.title} - {self.issuer}"
