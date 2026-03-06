from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
  list_display = ("title", "post_type", "is_published", "published_at", "created_at")
  list_filter = ("post_type", "is_published")
  search_fields = ("title", "excerpt", "content", "tags")
  prepopulated_fields = {"slug": ("title",)}
