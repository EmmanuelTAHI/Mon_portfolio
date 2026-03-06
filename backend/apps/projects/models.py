from django.db import models


class Project(models.Model):
  CATEGORY_CHOICES = [
      ("web", "Web Application"),
      ("app", "Mobile Application"),
      ("tool", "Security Tool"),
      ("script", "Automation / Script"),
      ("ctf", "CTF / Writeups"),
      ("other", "Other"),
  ]

  title = models.CharField(max_length=200)
  image = models.ImageField(upload_to="projects/", blank=True, null=True)
  slug = models.SlugField(max_length=220, unique=True)
  short_description = models.CharField(max_length=255)
  description = models.TextField()
  category = models.CharField(
      max_length=20,
      choices=CATEGORY_CHOICES,
      default="web",
  )
  technologies = models.CharField(
      max_length=300,
      help_text="Liste de technologies séparées par des virgules (ex: Python, Django, Nmap)",
  )
  github_url = models.URLField(blank=True, help_text="URL du dépôt GitHub")
  is_featured = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ["-created_at"]

  def __str__(self) -> str:
      return self.title
