"""
Django settings for Lider Avto (avto ehtiyot qismlar) project.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Serverda sozlamalar .env faylidan oqiladi (qarang: .env.example)
load_dotenv(BASE_DIR / ".env")


def _env_list(name):
    return [x.strip() for x in os.environ.get(name, "").split(",") if x.strip()]


# Lokal ishlab chiqishda: DJANGO_DEBUG=1 (start.sh o'zi qo'yadi). Serverda DEBUG o'chiq bo'ladi.
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"
    else:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY topilmadi. .env faylini yarating (.env.example ga qarang)."
        )

# Serverda: DJANGO_ALLOWED_HOSTS=sayt.uz,www.sayt.uz,1.2.3.4
ALLOWED_HOSTS = ["*"] if DEBUG else _env_list("DJANGO_ALLOWED_HOSTS")
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS bo'sh. .env ga domen yoki IP yozing.")

# HTTPS (certbot) o'rnatilgandan keyin .env ga DJANGO_HTTPS=1 qo'ying
HTTPS = os.environ.get("DJANGO_HTTPS", "0") == "1"
CSRF_TRUSTED_ORIGINS = _env_list("DJANGO_CSRF_TRUSTED_ORIGINS")  # masalan: https://sayt.uz
if HTTPS and not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Telegram bot — yangi buyurtma bildirishnomalari uchun
# .env ga yozing: TELEGRAM_BOT_TOKEN=..., TELEGRAM_CHAT_ID=...
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


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
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    # Local
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "dist"] if not DEBUG else [],
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
import dj_database_url

if os.environ.get("DATABASE_URL"):
    # Render PostgreSQL
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Custom User Model
AUTH_USER_MODEL = "main.CustomUser"


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


# Static & Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "frontend" / "dist" / "assets"] if not DEBUG else [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ─────────────────────────────────────────
# Django REST Framework
# ─────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "main.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# ─────────────────────────────────────────
# CORS
# ─────────────────────────────────────────
# Frontend va API bitta domenda (nginx) ishlaydi, shuning uchun serverda CORS yopiq.
# Kerak bo'lsa: DJANGO_CORS_ORIGINS=https://boshqa-sayt.uz
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = _env_list("DJANGO_CORS_ORIGINS")
CORS_ALLOW_CREDENTIALS = True


# ─────────────────────────────────────────
# drf-spectacular (Swagger)
# ─────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "Lider Avto API",
    "DESCRIPTION": """
**Lider Avto — avto ehtiyot qismlar do'koni, REST API**

## Autentifikatsiya
Token asosida autentifikatsiya ishlatiladi.

1. /api/auth/register/ — ro'yxatdan o'ting, token olasiz
2. /api/auth/login/ — kiring, token olasiz
3. Keyingi so'rovlarda: Authorization: Token <token> headerini yuboring

## Asosiy bo'limlar
- **Auth** — Ro'yxat, kirish, profil
- **Categories** — Mahsulot kategoriyalari
- **Products** — Mahsulot katalogi va narx hisoblash
- **Addresses** — Yetkazib berish manzillari
- **Cart** — Xarid savati
- **Orders** — Buyurtmalar
- **Admin** — Boshqaruv paneli (faqat admin)
    """,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [{"tokenAuth": []}],
}
