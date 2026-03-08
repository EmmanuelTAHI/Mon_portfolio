from django.conf import settings
from rest_framework import serializers

from .models import BlogPost


def _build_media_url(request, relative_path):
    if not relative_path or relative_path.startswith(("http://", "https://")):
        return relative_path
    path = (settings.MEDIA_URL if settings.MEDIA_URL.endswith("/") else settings.MEDIA_URL + "/") + relative_path
    if getattr(settings, "BACKEND_PUBLIC_URL", None):
        return settings.BACKEND_PUBLIC_URL.rstrip("/") + (path if path.startswith("/") else "/" + path)
    return request.build_absolute_uri(path) if request else path


class BlogPostSerializer(serializers.ModelSerializer):
  class Meta:
      model = BlogPost
      fields = "__all__"

  def to_representation(self, instance):
      data = super().to_representation(instance)
      request = self.context.get("request")
      if data.get("cover_image"):
          data["cover_image"] = _build_media_url(request, data["cover_image"])
      return data

