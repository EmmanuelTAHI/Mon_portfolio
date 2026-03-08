"""
Paramètres Django pour le projet config (API portfolio cybersécurité).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Charger les variables d'environnement depuis .env (développement)
load_dotenv(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# Voir https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-key-change-me",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    # Local apps
    "apps.projects",
    "apps.skills",
    "apps.experience",
    "apps.contact",
    "apps.certifications",
    "apps.ctf",
    "apps.blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "apps.ctf.middleware.DisableCSRFForCTF",  # Désactiver CSRF pour CTF avant le middleware CSRF
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# Si DATABASE_URL est défini (ex: Render), l'utiliser. Sinon PostgreSQL si DB_ENGINE=postgres, sinon SQLite.
_database_url = os.getenv("DATABASE_URL")
if _database_url:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(_database_url)}
elif os.getenv("DB_ENGINE") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "portfolio"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static & media files

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []
FIXTURE_DIRS = [BASE_DIR / "fixtures"]
# WhiteNoise: servir les fichiers statiques en production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Sur Render : à l'exécution le dossier media/ du repo n'est pas toujours disponible.
# Au build on copie media/* dans static/media/ ; en prod on sert les médias depuis là.
if os.getenv("RENDER_EXTERNAL_URL"):
    MEDIA_ROOT = STATIC_ROOT / "media"

# URL publique du backend pour construire les URLs des médias (images projets, etc.).
# En local : mettre BACKEND_PUBLIC_URL=http://localhost:8000 dans .env.
# Sur Render : Render définit automatiquement RENDER_EXTERNAL_URL (ex. https://portfolio-backend-xxx.onrender.com).
# On l'utilise en secours si BACKEND_PUBLIC_URL n'est pas défini.
BACKEND_PUBLIC_URL = (
    (os.getenv("BACKEND_PUBLIC_URL", "").strip() or os.getenv("RENDER_EXTERNAL_URL", "").strip()) or None
)


# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# CORS

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CSRF : origines de confiance (frontend sur Vercel). À définir sur Render, ex: https://ton-projet.vercel.app
CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if x.strip()]


# Email configuration (SMTP)

_smtp_user = os.getenv("SMTP_USER", "").strip()
if _smtp_user:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() == "true"
    EMAIL_USE_SSL = os.getenv("SMTP_USE_SSL", "False").lower() == "true"
    EMAIL_HOST_USER = _smtp_user
    EMAIL_HOST_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "30"))
    DEFAULT_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", _smtp_user)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@localhost")

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", DEFAULT_FROM_EMAIL)

if not _smtp_user and DEBUG:
    import logging
    logging.getLogger("config.settings").warning(
        "SMTP_USER is not set: contact form emails will only appear in the console, not in your mailbox. "
        "Set SMTP_USER and SMTP_PASSWORD in .env to receive emails (and set CONTACT_EMAIL to your inbox)."
    )


# drf-spectacular (OpenAPI / Swagger)

SPECTACULAR_SETTINGS = {
    "TITLE": "Portfolio API",
    "DESCRIPTION": "API du portfolio (projets, compétences, expérience, contact, certifications, CTF).",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# Cache configuration for rate limiting
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ctf-rate-limiting",
    }
}

# Logging: médias et API pour diagnostic sur Render
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps.projects.serializers": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
