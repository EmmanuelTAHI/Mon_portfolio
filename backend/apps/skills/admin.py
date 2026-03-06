from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "level", "created_at")
  list_filter = ("category",)
  search_fields = ("name", "description")
