import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
import sentry_sdk

sentry_sdk.init(
    dsn=(
        "https://38f01932ee1648b37247a241cb06f10e@o4506155887558656."
        "ingest.sentry.io/4506155889262592"
    ),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

load_dotenv(override=False)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "secret_key")

DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() in ("true", "1", "yes", "y")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(" ")

MAIL = os.getenv("DJANGO_MAIL", "example@mail.com")

ALLOW_REVERSE = os.getenv("DJANGO_ALLOW_REVERSE", "true").lower() in (
    "true",
    "1",
    "yes",
    "y",
)

USE_LOCAL_MEDIA = os.getenv("USE_LOCAL_MEDIA", "true").lower() in (
    "true",
    "1",
    "yes",
    "y",
)

STORAGE_NAME = os.getenv("STORAGE_NAME", "default").lower()

if STORAGE_NAME == "aws":
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

    AWS_LOCATION = "media/"

    AWS_S3_REGION_NAME = os.getenv("AWS_REGION")

    AWS_S3_FILE_OVERWRITE = False

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    }

    MEDIA_ROOT = (
        f"https://{AWS_STORAGE_BUCKET_NAME}{AWS_S3_REGION_NAME}"
        ".s3.amazonaws.com/{AWS_LOCATION}"
    )

MEDIA_URL = "/media/"

INSTALLED_APPS = [
    # Other
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "tinymce",
    "modeltranslation",
    # Main apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Developed apps
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
    "core.apps.CoreConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Other
    "django.middleware.locale.LocaleMiddleware",
    # Our middleware
    "lyceum.middleware.ReverseRussianMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = os.getenv("DJANGO_INTERNAL_IPS", "127.0.0.1").split(" ")

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DB_NAME = os.getenv("DB_NAME", "sqlite").lower()

if DB_NAME == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
elif DB_NAME == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRE_DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRE_DB_USER", "default"),
            "PASSWORD": os.getenv("POSTGRE_DB_PASSWORD", "password"),
            "HOST": os.getenv("POSTGRE_DB_HOST", "localhost"),
            "PORT": os.getenv("POSTGRE_DB_PORT", "5432"),
        },
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "ru"

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = os.getenv("STATIC_URL", "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

THUMBNAIL_PRESERVE_FORMAT = True

THUMBNAIL_REDIS_URL = os.getenv("REDIS_URL", None)

if THUMBNAIL_REDIS_URL:
    THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.redis_kvstore.KVStore"

THUMBNAIL_STORAGE = "django.core.files.storage.FileSystemStorage"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"

DEPLOYING_ON_HTTPS = os.getenv("DEPLOYING_ON_HTTPS", "false").lower() in (
    "true",
    "1",
    "yes",
    "y",
)

if DEPLOYING_ON_HTTPS:
    SECURE_HSTS_SECONDS = True

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True
