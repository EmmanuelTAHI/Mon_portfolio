from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Project
from .serializers import ProjectSerializer


class ProjectPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  lookup_field = "slug"
  lookup_url_kwarg = "slug"
  pagination_class = ProjectPagination

