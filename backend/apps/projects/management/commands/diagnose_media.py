"""
Commande de diagnostic pour les images des projets (médias).
À lancer sur Render en build ou manuellement : python manage.py diagnose_media

Affiche :
- MEDIA_ROOT, MEDIA_URL, BACKEND_PUBLIC_URL, RENDER_EXTERNAL_URL
- Contenu du dossier media/projects/
- Pour chaque projet : image en DB, chemin fichier, existe ?, URL retournée par l'API
- Une URL de test à ouvrir dans le navigateur
"""
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.projects.models import Project


class Command(BaseCommand):
    help = "Diagnostique pourquoi les images des projets ne s'affichent pas (médias, URLs, fichiers)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            type=str,
            default=None,
            help="URL de base du backend (ex: https://portfolio-backend-i4rb.onrender.com) pour afficher les URLs de test.",
        )

    def handle(self, *args, **options):
        base_url = (options.get("base_url") or "").strip()

        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write(self.style.HTTP_INFO("  DIAGNOSTIC IMAGES PROJETS (médias)"))
        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write("")

        # 1. Configuration
        self.stdout.write(self.style.WARNING("[1] CONFIGURATION"))
        self.stdout.write("")
        media_root = getattr(settings, "MEDIA_ROOT", None)
        media_url = getattr(settings, "MEDIA_URL", "")
        backend_public = getattr(settings, "BACKEND_PUBLIC_URL", None)
        render_external = os.getenv("RENDER_EXTERNAL_URL", "").strip()

        self.stdout.write(f"  MEDIA_ROOT           = {media_root}")
        self.stdout.write(f"  MEDIA_URL            = {media_url}")
        self.stdout.write(f"  BACKEND_PUBLIC_URL   = {backend_public or '(non défini)'}")
        self.stdout.write(f"  RENDER_EXTERNAL_URL  = {render_external or '(non défini)'}")
        self.stdout.write("")

        # Quelle base est utilisée pour les URLs ?
        effective_base = backend_public or render_external or None
        if effective_base:
            self.stdout.write(self.style.SUCCESS(f"  -> Base utilisée pour les URLs d'images : {effective_base}"))
        else:
            self.stdout.write(
                self.style.ERROR("  -> ATTENTION : aucune base d'URL (BACKEND_PUBLIC_URL ni RENDER_EXTERNAL_URL).")
            )
            self.stdout.write(
                self.style.ERROR("     Les URLs d'images seront relatives ou incorrectes.")
            )
        self.stdout.write("")

        # 2. Dossier media
        self.stdout.write(self.style.WARNING("[2] DOSSIER MEDIA (fichiers sur le disque)"))
        self.stdout.write("")
        if not media_root:
            self.stdout.write(self.style.ERROR("  MEDIA_ROOT est vide."))
        else:
            media_root_path = Path(media_root)
            self.stdout.write(f"  Chemin résolu : {media_root_path.resolve()}")
            self.stdout.write(f"  Existe ?      {media_root_path.exists()}")
            if media_root_path.exists():
                projects_dir = media_root_path / "projects"
                self.stdout.write(f"  media/projects existe ? {projects_dir.exists()}")
                if projects_dir.exists():
                    files = list(projects_dir.iterdir())
                    self.stdout.write(f"  Fichiers dans media/projects/ ({len(files)}) :")
                    for f in sorted(files):
                        self.stdout.write(f"    - {f.name}  ({f.stat().st_size} octets)")
                else:
                    self.stdout.write(self.style.ERROR("  Le dossier media/projects/ n'existe pas."))
            else:
                self.stdout.write(self.style.ERROR("  Le dossier MEDIA_ROOT n'existe pas."))
        self.stdout.write("")

        # 3. Projets en base et URLs
        self.stdout.write(self.style.WARNING("[3] PROJETS EN BASE ET URLS D'IMAGES"))
        self.stdout.write("")
        projects = Project.objects.all().order_by("id")
        if not projects.exists():
            self.stdout.write("  Aucun projet en base.")
        else:
            for p in projects:
                self.stdout.write(f"  Projet id={p.id}  slug={p.slug}")
                image_field = getattr(p, "image", None)
                if not image_field:
                    self.stdout.write("    image (champ) : vide")
                    self.stdout.write("")
                    continue
                rel = getattr(image_field, "name", None) or str(image_field) or ""
                self.stdout.write(f"    image (en DB) : {rel!r}")
                if not rel:
                    self.stdout.write("")
                    continue
                full_path = Path(settings.MEDIA_ROOT) / rel
                exists = full_path.exists()
                self.stdout.write(f"    chemin fichier : {full_path}")
                self.stdout.write(f"    fichier existe : {exists}")
                # URL que l'API renverrait (même logique que le serializer)
                url = self._build_media_url(rel)
                self.stdout.write(f"    URL API        : {url}")
                if not exists:
                    self.stdout.write(self.style.ERROR("    -> FICHIER MANQUANT : l'image ne s'affichera pas."))
                self.stdout.write("")
        self.stdout.write("")

        # 4. URL de test
        self.stdout.write(self.style.WARNING("[4] TEST MANUEL"))
        self.stdout.write("")
        test_base = base_url or effective_base
        if test_base and projects.exists():
            first = projects.first()
            rel = getattr(first.image, "name", None) if first.image else None
            if rel:
                test_url = test_base.rstrip("/") + "/" + media_url.strip("/") + "/" + rel
                self.stdout.write("  Ouvre cette URL dans ton navigateur (premier projet) :")
                self.stdout.write(self.style.SUCCESS(f"  {test_url}"))
                self.stdout.write("")
                self.stdout.write("  Si tu vois l'image -> le backend sert bien les médias.")
                self.stdout.write("  Si 404 -> le fichier manque ou MEDIA_ROOT est mauvais.")
        else:
            self.stdout.write("  Indique --base-url=https://portfolio-backend-i4rb.onrender.com pour afficher une URL de test.")
        self.stdout.write("")
        self.stdout.write(self.style.HTTP_INFO("=" * 70))

    def _build_media_url(self, relative_path):
        """Reproduit la logique du serializer pour afficher l'URL exacte."""
        if not relative_path or not relative_path.strip():
            return None
        relative_path = relative_path.strip()
        if relative_path.startswith(("http://", "https://")):
            return relative_path
        media_url = (
            settings.MEDIA_URL
            if settings.MEDIA_URL.endswith("/")
            else settings.MEDIA_URL + "/"
        )
        path = (
            (media_url + relative_path)
            if not relative_path.startswith("/")
            else (settings.MEDIA_URL.rstrip("/") + relative_path)
        )
        base = getattr(settings, "BACKEND_PUBLIC_URL", None)
        if base:
            base = base.rstrip("/")
            return base + (path if path.startswith("/") else "/" + path)
        return path
