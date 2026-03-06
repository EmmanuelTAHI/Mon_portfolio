from rest_framework import serializers

from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
  class Meta:
      model = BlogPost
      fields = "__all__"

  def to_representation(self, instance):
      data = super().to_representation(instance)
      request = self.context.get("request")
      if request and data.get("cover_image"):
          data["cover_image"] = request.build_absolute_uri(data["cover_image"])
      return data

