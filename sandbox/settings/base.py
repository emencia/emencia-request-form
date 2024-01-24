"""
Base Django settings for sandbox
"""

from pathlib import Path

from django import VERSION


SECRET_KEY = "***TOPSECRET***"


# Project paths
BASE_DIR = Path(__file__).parents[2]
PROJECT_PATH = BASE_DIR / "sandbox"
VAR_PATH = BASE_DIR / "var"

DEBUG = False

# Https is never enabled on default and development environment, only for
# integration and production.
HTTPS_ENABLED = False

ADMINS = (
    # ("Admin", "PUT_ADMIN_EMAIL_HERE"),
)

MANAGERS = ADMINS

DATABASES = {}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "America/Chicago"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
    ('fr', "Français"),
)

# A tuple of directories where Django looks for translation files
LOCALE_PATHS = [
    PROJECT_PATH / "locale",
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = VAR_PATH / "media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = VAR_PATH / "static"

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH / "static-sources",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "sandbox.urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "sandbox.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_PATH / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": False,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Ensure we can override applications widgets templates from project template
# directory, require also 'django.forms' in INSTALLED_APPS
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Default SMTP configuration don't send any email for real and just push them to the
# console output
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = None
EMAIL_PORT = None


"""
DjangoCMS configuration
"""

# Admin style need to be put before Django admin
INSTALLED_APPS[0:0] = [
    "djangocms_admin_style",
]

# Enable CMS required apps
INSTALLED_APPS.extend([
    "cms",
    "treebeard",
    "menus",
    "sekizai",
    "djangocms_text_ckeditor",
])

# Enable CMS middlewares
MIDDLEWARE.extend([
    "cms.middleware.utils.ApphookReloadMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
])

# Required since DjangoCMS 3.7.2
X_FRAME_OPTIONS = "SAMEORIGIN"

# Enable required cms context processors
TEMPLATES[0]["OPTIONS"]["context_processors"].extend([
    "sekizai.context_processors.sekizai",
    "cms.context_processors.cms_settings",
])

# Define cms page templates
CMS_TEMPLATES = [
    ("pages/default.html", "Default"),
]


"""
django-simple-captcha configuration
"""
INSTALLED_APPS.extend([
    "captcha",
])

# Lifespan in minutes of the generated captcha.
CAPTCHA_TIMEOUT = 5


"""
 django-phonenumber-field configuration
"""
INSTALLED_APPS.extend([
    "phonenumber_field",
])


PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

"""
Crispy forms configuration
"""
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

INSTALLED_APPS.extend([
    "crispy_forms",
    "crispy_bootstrap5",
])


"""
Request-form configuration
"""
from request_form.settings import *  # noqa: E402,F401,F403

INSTALLED_APPS.extend([
    "request_form",
])
