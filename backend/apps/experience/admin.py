from django.contrib import admin

from .models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
  list_display = ("title", "organization", "experience_type", "start_date", "end_date", "is_current")
  list_filter = ("experience_type", "is_current")
  search_fields = ("title", "organization", "description")
  ordering = ("order", "-start_date")
