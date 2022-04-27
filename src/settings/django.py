import os

from pathlib import Path

from django.core.management.utils import get_random_secret_key

import dj_database_url

from .environment import env


BASE_DIR = Path(__file__).resolve().parent.parent


def rel(*path):
    return BASE_DIR.joinpath(*path)


DEBUG = os.getenv("DEBUG", default="True")

INTERNAL_IPS = env.list("SRC_INTERNAL_IPS", default=[])

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", default="0.0.0.0,127.0.0.1,localhost").split(",")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default=get_random_secret_key())

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "rest_framework",
    "django_extensions",
    "django_filters",
    "drf_yasg",
    # our apps
    "src.apps.common",
    "src.apps.accounts",
] + env.list("SRC_DEV_INSTALLED_APPS", default=[])

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
] + env.list("SRC_DEV_MIDDLEWARE", default=[])

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [rel("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "src.wsgi.application"

if os.getenv("DATABASE_URL", default=None) is not None:
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }
else:
    DATABASES = {
        "default": dj_database_url.parse("postgresql://postgres:awesome_password_1@localhost:5432/src_db"),
    }

AUTH_USER_MODEL = "accounts.UserAccount"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SECURE_BROWSER_XSS_FILTER = env.bool("SRC_SECURE_BROWSER_XSS_FILTER", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SRC_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SESSION_COOKIE_HTTPONLY = env.bool("SRC_SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_SECURE = env.bool("SRC_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("SRC_CSRF_COOKIE_SECURE", default=True)
X_FRAME_OPTIONS = env.str("SRC_X_FRAME_OPTIONS", default="SAMEORIGIN")
SECURE_HSTS_SECONDS = env.int("SRC_SECURE_HSTS_SECONDS", default=31536000)  # 1 year
SESSION_COOKIE_NAME = "s"
CSRF_COOKIE_NAME = "c"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [rel("..", "..", "api", "locale")]

STATIC_URL = env.str("SRC_STATIC_URL", default="/s/")
STATIC_ROOT = env.str("SRC_STATIC_ROOT", default=rel("..", "public", "static"))

MEDIA_URL = env.str("SRC_MEDIA_URL", default="/m/")
MEDIA_ROOT = env.str("SRC_MEDIA_ROOT", rel("..", "public", "media"))

EMAIL_BACKEND = env.str("SRC_EMAIL_BACKEND", default=None)
if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":  # pragma: no cover
    EMAIL_HOST = env.str("SRC_EMAIL_HOST")
    EMAIL_PORT = env.str("SRC_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("SRC_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("SRC_EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env.bool("SRC_EMAIL_USE_TLS", default=True)

SITE_ID = env.int("SRC_SITE_ID", default=1)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

APPEND_SLASH = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
