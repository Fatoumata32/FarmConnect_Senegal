from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-changez-moi-en-production')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.farmconnect.sn']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
    'farmconnect_app',
    'weather',
    'crops',
    'community',
    'advice',
    'marketplace',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware personnalisé (optionnel)
    # 'farmconnect_app.middleware.UserActivityMiddleware',
]

ROOT_URLCONF = 'farmconnect_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'farmconnect_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'farmconnect.sqlite3',
    }
}

# ==================================
# PARAMÈTRES D'AUTHENTIFICATION
# ==================================

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'farmconnect_app.User'

# URLs de redirection
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Paramètres de session
SESSION_COOKIE_AGE = 1209600  # 2 semaines
SESSION_COOKIE_NAME = 'farmconnect_sessionid'
SESSION_COOKIE_SECURE = False  # True en production avec HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Paramètres de sécurité des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================================
# MESSAGES FRAMEWORK
# ==================================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ==================================
# INTERNATIONALISATION
# ==================================

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('wo', 'Wolof'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ==================================
# FICHIERS STATIQUES ET MÉDIA
# ==================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================================
# CONFIGURATION APIS EXTERNES
# ==================================

# API Keys - Load from environment variables for security
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY', default='')
WEATHERAPI_KEY = config('WEATHERAPI_KEY', default='')  # Pour WeatherAPI.com
SMS_API_KEY = config('SMS_API_KEY', default='')

# ==================================
# CRISPY FORMS
# ==================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==================================
# REST FRAMEWORK
# ==================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# ==================================
# CELERY CONFIGURATION
# ==================================

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ==================================
# EMAIL (pour la réinitialisation de mot de passe)
# ==================================

# Configuration SMTP pour les emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'f.ndiaye@alustudent.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'FarmConnect Senegal <f.ndiaye@alustudent.com>'

# ==================================
# SÉCURITÉ ET CORS
# ==================================

# Paramètres CSRF
CSRF_COOKIE_SECURE = False  # True en production avec HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = 'farmconnect_csrftoken'

# Paramètres de sécurité généraux
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Referrer Policy - Don't leak referrer info to third parties
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Cross-Origin Opener Policy
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# CORS Headers
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# En production, décommentez ces lignes :
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ==================================
# LOGGING
# ==================================

# Créez le dossier logs s'il n'existe pas
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'farmconnect.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'auth_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'auth.log',
            'maxBytes': 1024*1024*2,  # 2 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'farmconnect_app': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['auth_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.contrib.auth': {
            'handlers': ['auth_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ==================================
# CONFIGURATION CACHE (REDIS)
# ==================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'KEY_PREFIX': 'farmconnect',
        'TIMEOUT': 300,  # 5 minutes
        'VERSION': 1,
    }
}

# ==================================
# CONFIGURATION SPÉCIFIQUE À FARMCONNECT
# ==================================

# Paramètres météo
WEATHER_UPDATE_INTERVAL = 3600  # 1 heure en secondes
WEATHER_CACHE_TIMEOUT = 1800    # 30 minutes

# Paramètres d'upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Paramètres de l'application
FARMCONNECT_VERSION = '1.0.0'
FARMCONNECT_COMPANY = 'FarmConnect Senegal'
FARMCONNECT_SUPPORT_EMAIL = 'support@farmconnect.sn'

# Régions du Sénégal
SENEGAL_REGIONS = [
    ('dakar', 'Dakar'),
    ('thies', 'Thiès'),
    ('saint-louis', 'Saint-Louis'),
    ('diourbel', 'Diourbel'),
    ('louga', 'Louga'),
    ('fatick', 'Fatick'),
    ('kaolack', 'Kaolack'),
    ('kaffrine', 'Kaffrine'),
    ('tambacounda', 'Tambacounda'),
    ('kedougou', 'Kédougou'),
    ('kolda', 'Kolda'),
    ('sedhiou', 'Sédhiou'),
    ('ziguinchor', 'Ziguinchor'),
    ('matam', 'Matam'),
]

# Rôles utilisateur
USER_ROLES = [
    ('farmer', 'Agriculteur'),
    ('expert', 'Expert Agricole'),
    ('investor', 'Investisseur'),
    ('supplier', 'Fournisseur'),
    ('admin', 'Administrateur'),
]

# ==================================
# CONFIGURATION ENVIRONNEMENT DE DÉVELOPPEMENT
# ==================================

if DEBUG:
    # Django Debug Toolbar (optionnel)
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
    except ImportError:
        pass
    
    # Désactiver la mise en cache en développement
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'