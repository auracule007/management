import os
from datetime import timedelta
from pathlib import Path
from celery.schedules import crontab
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-g^(k(ph4lghw3n@e9gw6_7vf)or=sf3h&8ix!&ln_03#7!m3t4"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["https://codedexteracademy.onrender.com", "*"]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "subscriptions",
    "promotion",
    "quiz.apps.QuizConfig",
    "forum.apps.ForumConfig",
    "lesson.apps.LessonConfig",
    "performance.apps.PerformanceConfig",
    "useractivity.apps.UseractivityConfig",
    "analytics.apps.AnalyticsConfig",
    "gamification.apps.GamificationConfig",
    "register.apps.RegisterConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "django_filters",
    "drf_yasg",
    "corsheaders",
    # pip install django djangorestframework djoser django-fliter drf_yasg django-allauth
    "mail_templated",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # white noise middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # account
    "api.middleware.CourseViewCountMiddleware",  # CUSTOM MIDDLEWARE
]

ROOT_URLCONF = "management.urls"

AUTH_USER_MODEL = "api.User"

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
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "management.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 20
}
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('NAME'),
#         'USER': config('USER'),
#         'PASSWORD': config('PASSWORD'),
#         'HOST': '127.0.0.1',  # Or the IP address of your PostgreSQL server
#         'PORT': 5432,        # Or the port your PostgreSQL server is listening on
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "management/static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
    "COERCE_DECIMAL_TO_STRING": False,
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "TOKEN_OBTAIN_SERIALIZER": "api.serializers.UserTokenObtainPairSerializer",
}



DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "api.serializers.UserCreateSerializer",
        "user": "api.serializers.UserSerializer",
        "current_user": "api.serializers.UserSerializer",
        "password_reset": "djoser.serializers.SendEmailResetSerializer",
        "password_reset_confirm": "djoser.serializers.PasswordResetConfirmSerializer",
    },
}

SITE_ID = 1

# SSO authentication integration
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}

# LOGIN_REDIRECT_URL = "/"

# SSO authentication integration done
LOGIN_REDIRECT_URL = "/api/courses"
SIGNUP_REDIRECT_URL = "/auth/jwt/create"
# SSO authentication integration done

# mail configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER = "2f9852130e042b"
EMAIL_HOST_PASSWORD = "c6b7c90c5013d9"
EMAIL_PORT = 2525
EMAIL_USE_TSL = True

APPEND_SLASH = False
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "https://dexter9ja.vercel.app",
    "http://localhost:3000",
]

# my development settings configuration
# try:
#     from .dev import *
# except ImportError:
#     pass


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "mainroot.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",
        }
    },
}


FLUTTER_SECRET_KEY = "FLWSECK_TEST-f2ba505a6d90061af98b8cb4281e01c3-X"
# FLUTTER_SECRET_KEY = config("FLUTTER_SECRET_KEY")
# PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID")
# PAYPAL_SECRET = config("PAYPAL_SECRET")
# PAYPAL_BASE_URL = config("PAYPAL_BASE_URL")

# STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
# STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
# STRIPE_BASE_URL = "https://api.stripe.com"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = "redis://localhost:6379/1"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_BEAT_SCHEDULE = {
  "check-sub-expiration-every-minute": {
    "task": "subscriptions.tasks.check_sub_expiration",
    "schedule": crontab(minute="*")
  },
  "check-course-start-date-every-minute": {
    "task": "api.tasks.check_course_start_date",
    "schedule": crontab(minute="*")
  },
  "check-expiration-notification-every-minute": {
    "task": "subscriptions.tasks.check_expiration_notification",
    "schedule": crontab(minute="*")
  },
  "check-promotion-is-schedule-every-minute": {
    "task": "promotion.tasks.promotion_management",
    "schedule": crontab(minute="*")
  },
}

# code editor
CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = config('CLIENT_SECRET')

