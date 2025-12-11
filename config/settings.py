import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DB_PASSWORD")


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# -------------------------------------------------------------------
# Basic: secrets & debug (use environment variables)
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Basic: secrets & debug (use environment variables)
# -------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-this")
# To run locally with DEBUG on, set DJANGO_DEBUG=True in your env.
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    "https://ecommerce-backend-12-q8sv.onrender.com",
]


# -------------------------------------------------------------------
# Installed apps / middleware (keeps your current apps)
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "corsheaders",

    # Local apps
    "products",
    "orders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",              # must be high in order
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",         # serve static securely
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ALLOW_ALL_ORIGINS =  "http://localhost:5173",

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# -------------------------------------------------------------------
# Templates
# -------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],   # add paths if you use server-rendered templates
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

# -------------------------------------------------------------------
# Database configuration:
# -------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if os.getenv("RENDER"):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ecommerce',
            'USER': 'postgres',
            'PASSWORD': 'DB_PASSWORD',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# -------------------------------------------------------------------
# REST Framework (keeps your JWT config; modify if you want anonymous orders)
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # You can add DEFAULT_PERMISSION_CLASSES if needed
}

# -------------------------------------------------------------------
# Authentication backends
# -------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# -------------------------------------------------------------------
# Password validation (keep minimal or default)
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static & media files (WhiteNoise for static)
# -------------------------------------------------------------------
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Static files
# ------------------------

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"  # or str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"

# -------------------------------------------------------------------
# CORS (keep open in dev, restrict in production)
# -------------------------------------------------------------------
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # In production, set DJANGO_CORS_ALLOWED_ORIGINS to comma separated origins
    raw = os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "")
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    CORS_ALLOWED_ORIGINS = origins
    CORS_ALLOW_CREDENTIALS = True

# -------------------------------------------------------------------
# Security headers & cookie settings for production
# -------------------------------------------------------------------
# Only enable the following when DEBUG is False and you use HTTPS (recommended)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("1", "true", "yes")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 60 * 60 * 24 * 30))  # 30 days by default
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
    X_FRAME_OPTIONS = "DENY"
else:
    # Development friendly defaults
    SECURE_SSL_REDIRECT = False

# -------------------------------------------------------------------
# Logging (basic)
# -------------------------------------------------------------------
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}

# -------------------------------------------------------------------
# Other helpful environment flags
# -------------------------------------------------------------------
# Example: RENDER will set an env var; if you host elsewhere, adapt.
ON_RENDER = os.environ.get("RENDER", "") != ""

# -------------------------------------------------------------------
# End of settings
# -------------------------------------------------------------------
