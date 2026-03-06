from django.db import models


class ContactMessage(models.Model):
  name = models.CharField(max_length=150)
  email = models.EmailField()
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)
  source = models.CharField(
      max_length=100,
      blank=True,
      help_text="Contexte (portfolio, blog, autre)",
  )
  user_agent = models.CharField(max_length=300, blank=True)

  class Meta:
      ordering = ["-created_at"]

  def __str__(self) -> str:
      return f"{self.name} <{self.email}>"
