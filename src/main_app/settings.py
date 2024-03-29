"""
Django settings for asu django project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import datetime
import os
from pathlib import Path

from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("APP_SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": DB_HOST,
        "PORT": 5432,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "NAME": DB_NAME,
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "user",
    "api",
]
AUTH_USER_MODEL = "user.User"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

]

ROOT_URLCONF = "main_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "main_app.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa e501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa e501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa e501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa e501
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    "DATE_FORMAT": "%d-%m-%Y",
    "DATETIME_FORMAT": "%d-%m-%Y %H:%M",
    "DATETIME_INPUT_FORMATS": ["%d.%m.%Y"],
    'EXCEPTION_HANDLER': 'api.utils.exception_handler.custom_exception_handler'
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
}

LOGGING = {
    # ...
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
        },
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            # 'formatter': 'json',
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "loggers": {
            "django.db.backends": {
                "level": "INFO",
            },
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


CORS_ALLOW_HEADERS = default_headers + (
    "access-control-allow-headers",
    "access-control-allow-credentials",
)

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://db"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
FILES_URL = "/files/"
FILES_ROOT = os.path.join(BASE_DIR, "files")
MEDIA_FILES_DIR = "media_files"
