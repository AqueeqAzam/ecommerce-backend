import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


# -------------------------------------------------------------------
# Basic: secrets & debug (use environment variables)
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Basic: secrets & debug (use environment variables)
# -------------------------------------------------------------------

# To run locally with DEBUG on, set DJANGO_DEBUG=True in your env.
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

# ------------------------------------------------------------------
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


CORS_ALLOWED_ORIGINS = [
    "https://gilded-pegasus-ca4bb4.netlify.app",
]

CORS_ALLOW_ALL_HEADERS = True


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

# Render sets this automatically
RENDER = os.environ.get("RENDER")

# Get database URL from env
DATABASE_URL = os.environ.get("DB_INTERNAL_URL")

if RENDER and DATABASE_URL:
    # Production: Render
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "ecommerce",
            "USER": "postgres",
            "PASSWORD": "DB_PASSWORD",
            "HOST": "localhost",
            "PORT": "5432",
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

# ------------------------
# Static files
# ------------------------

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"  # or str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

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
