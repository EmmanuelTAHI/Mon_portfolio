from django.db import models


class Experience(models.Model):
  EXPERIENCE_TYPE_CHOICES = [
      ("education", "Education"),
      ("lab", "Personal Lab"),
      ("ctf", "CTF / Competition"),
      ("work", "Professional Experience"),
      ("project", "Project"),
      ("certification", "Certification"),
  ]

  title = models.CharField(max_length=200)
  organization = models.CharField(max_length=200)
  experience_type = models.CharField(
      max_length=20,
      choices=EXPERIENCE_TYPE_CHOICES,
      default="education",
  )
  location = models.CharField(max_length=150, blank=True)
  start_date = models.DateField()
  end_date = models.DateField(blank=True, null=True)
  is_current = models.BooleanField(default=False)
  description = models.TextField()
  order = models.PositiveIntegerField(default=0, help_text="Ordre sur la timeline")
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
      ordering = ["order", "-start_date"]

  def __str__(self) -> str:
      return f"{self.title} - {self.organization}"
