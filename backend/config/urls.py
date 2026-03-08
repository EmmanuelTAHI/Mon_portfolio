from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    """Point d'entrée /api/ pour vérifier que le backend est en ligne."""
    return JsonResponse({
        "message": "Backend fonctionne !",
        "api": "Portfolio API",
        "docs": "/api/docs/",
        "schema": "/api/schema/",
        "routes": [
            "/api/projects/",
            "/api/skills/",
            "/api/experience/",
            "/api/contact/",
            "/api/certifications/",
            "/api/ctf/",
            "/api/blog/",
        ],
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/projects/", include("apps.projects.urls")),
    path("api/skills/", include("apps.skills.urls")),
    path("api/experience/", include("apps.experience.urls")),
    path("api/contact/", include("apps.contact.urls")),
    path("api/certifications/", include("apps.certifications.urls")),
    path("api/ctf/", include("apps.ctf.urls")),
    path("api/blog/", include("apps.blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# En production, servir les médias (images projets, CTF) depuis MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
