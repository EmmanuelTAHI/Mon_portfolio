from rest_framework import serializers

from .models import Certification


class CertificationSerializer(serializers.ModelSerializer):
  class Meta:
      model = Certification
      fields = "__all__"

  def to_representation(self, instance):
      data = super().to_representation(instance)
      request = self.context.get("request")
      if request and data.get("credential_url"):
          data["credential_url"] = request.build_absolute_uri(data["credential_url"]) if not data["credential_url"].startswith("http") else data["credential_url"]
      return data
