"""
Middleware pour désactiver CSRF pour certains endpoints API publics (CTF, contact).
"""
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForCTF(MiddlewareMixin):
    """Désactive CSRF pour les endpoints /api/ctf/ et /api/contact/ (formulaire public)."""

    PUBLIC_API_PREFIXES = ("/api/ctf/", "/api/contact/")

    def process_request(self, request):
        if any(request.path.startswith(prefix) for prefix in self.PUBLIC_API_PREFIXES):
            setattr(request, "_dont_enforce_csrf_checks", True)
        return None
