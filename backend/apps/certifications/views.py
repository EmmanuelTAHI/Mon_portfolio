from rest_framework import viewsets

from .models import Certification
from .serializers import CertificationSerializer


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
  """
  Endpoint en lecture seule pour récupérer les certifications.
  """

  queryset = Certification.objects.all()
  serializer_class = CertificationSerializer
