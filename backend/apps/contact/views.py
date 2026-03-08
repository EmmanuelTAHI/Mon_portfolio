import logging
import os
from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.http import HttpRequest
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  """
  Endpoint pour recevoir les messages du formulaire de contact.
  Envoie un email via SMTP et sauvegarde le message en base.
  """

  queryset = ContactMessage.objects.all()
  serializer_class = ContactMessageSerializer

  def create(self, request: HttpRequest, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      recipient_email = os.getenv("CONTACT_EMAIL", getattr(settings, "DEFAULT_FROM_EMAIL", ""))
      recipient_email = (recipient_email or "").strip()

      if not recipient_email:
          logger.warning("CONTACT_EMAIL is not set; contact emails cannot be sent.")
          return Response(
              {
                  "detail": "Email delivery is not configured. Please try again later or use the social links below.",
                  "code": "smtp_not_configured",
              },
              status=status.HTTP_503_SERVICE_UNAVAILABLE,
          )

      contact_message = serializer.save(
          source="portfolio",
          user_agent=request.META.get("HTTP_USER_AGENT", "")[:300],
      )

      subject = f"[Portfolio Contact] Message from {contact_message.name}"
      body = f"""
Nouveau message depuis le formulaire de contact:

Nom: {contact_message.name}
Email: {contact_message.email}

Message:
{contact_message.message}

---
Date: {contact_message.created_at}
Source: {contact_message.source}
      """.strip()

      try:
          connection = get_connection(fail_silently=False)
          send_mail(
              subject=subject,
              message=body,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[recipient_email],
              connection=connection,
              fail_silently=False,
          )
      except Exception as e:
          logger.exception("SMTP send failed for contact message id=%s: %s", contact_message.id, str(e))
          return Response(
              {
                  "detail": "Unable to send email. Please try again later or use the social links below.",
                  "code": "smtp_error",
              },
              status=status.HTTP_503_SERVICE_UNAVAILABLE,
          )

      headers = self.get_success_headers(serializer.data)
      return Response(
          {"message": "Votre message a été envoyé avec succès.", "id": contact_message.id},
          status=status.HTTP_201_CREATED,
          headers=headers,
      )
