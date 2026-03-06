from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
      model = Project
      fields = "__all__"

  def to_representation(self, instance):
      data = super().to_representation(instance)
      request = self.context.get("request")
      if request:
          if data.get("image"):
              data["image"] = request.build_absolute_uri(data["image"])
          # Mapper repo_url vers github_url pour compatibilité si github_url est vide
          if not data.get("github_url") and data.get("repo_url"):
              data["github_url"] = data.get("repo_url", "")
      return data

