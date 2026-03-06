from django.db import models


class BlogPost(models.Model):
  POST_TYPE_CHOICES = [
      ("article", "Article"),
      ("ctf", "CTF Writeup"),
      ("tutorial", "Tutorial"),
      ("note", "Note"),
  ]

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=260, unique=True)
  post_type = models.CharField(
      max_length=20,
      choices=POST_TYPE_CHOICES,
      default="article",
  )
  excerpt = models.CharField(max_length=300, blank=True)
  content = models.TextField()
  cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
  tags = models.CharField(
      max_length=300,
      blank=True,
      help_text="Tags séparés par des virgules (ex: web, xss, burp)",
  )
  is_published = models.BooleanField(default=True)
  published_at = models.DateTimeField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ["-published_at", "-created_at"]

  def __str__(self) -> str:
      return self.title
