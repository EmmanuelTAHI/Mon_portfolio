from django.contrib import admin

from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
  list_display = ("title", "issuer", "status", "date", "created_at")
  list_filter = ("status", "issuer")
  search_fields = ("title", "issuer", "description")
  date_hierarchy = "date"
