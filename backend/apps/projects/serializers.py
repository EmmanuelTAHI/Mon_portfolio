from django.conf import settings
import logging
from rest_framework import serializers

from .models import Project

logger = logging.getLogger(__name__)


def _build_media_url(request, relative_path):
    """Construit une URL absolue pour un fichier média.
    Utilise BACKEND_PUBLIC_URL si défini (recommandé en dev et prod), sinon request.build_absolute_uri.
    """
    if not relative_path or not relative_path.strip():
        return None
    relative_path = relative_path.strip()
    if relative_path.startswith(("http://", "https://")):
        return relative_path
    media_url = (settings.MEDIA_URL if settings.MEDIA_URL.endswith("/") else settings.MEDIA_URL + "/")
    path = (media_url + relative_path) if not relative_path.startswith("/") else (settings.MEDIA_URL.rstrip("/") + relative_path)
    if getattr(settings, "BACKEND_PUBLIC_URL", None):
        base = settings.BACKEND_PUBLIC_URL.rstrip("/")
        full_url = base + path if path.startswith("/") else base + "/" + path
        logger.debug("Media URL: %s -> %s", relative_path, full_url)
        return full_url
    if request:
        full_url = request.build_absolute_uri(path)
        logger.debug("Media URL (request): %s -> %s", relative_path, full_url)
        return full_url
    logger.warning("Media path has no request and BACKEND_PUBLIC_URL not set: %s", relative_path)
    return path  # relatif


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
      model = Project
      fields = "__all__"

  def to_representation(self, instance):
      data = super().to_representation(instance)
      request = self.context.get("request")
      if data.get("image"):
          data["image"] = _build_media_url(request, data["image"])
          if data["image"] and instance.image:
              rel = getattr(instance.image, "name", None) or str(instance.image)
              full_path = settings.MEDIA_ROOT / rel
              exists = full_path.exists()
              if not exists:
                  logger.warning("Project image file missing: %s (MEDIA_ROOT=%s)", full_path, settings.MEDIA_ROOT)
              else:
                  logger.info("Project image resolved: %s", rel)
      if not data.get("github_url") and data.get("repo_url"):
          data["github_url"] = data.get("repo_url", "")
      return data

