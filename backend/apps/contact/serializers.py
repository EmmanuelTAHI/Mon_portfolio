from rest_framework import serializers

from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
  class Meta:
      model = ContactMessage
      fields = "__all__"
      read_only_fields = ("created_at", "is_read", "source", "user_agent")
      extra_kwargs = {
          "message": {"help_text": "Message content (minimum 10 characters)."},
      }

  def validate_name(self, value):
      if not value or len(value.strip()) < 2:
          raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
      return value.strip()

  def validate_email(self, value):
      if not value:
          raise serializers.ValidationError("L'email est requis.")
      return value.strip().lower()

  def validate_message(self, value):
      if not value or len(value.strip()) < 10:
          raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
      return value.strip()