
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGUAGES = [('nl', 'Nederlands')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w6**ci+meh=n)o_2ee5qga7ubb&pb30=iyx^5$+v-_iv+u)!nw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    # Third party apps
    'rest_framework',
    'django_filters',
    # Internal apps
    'supdem',
    'doj',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'scrum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scrum.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

USE_MYSQL = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'scrum',
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'nl'

MAX_ITEMS_IN_LIST=10

ITEM_LIFETIME_IN_DAYS=30

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'supdem.MyUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/'
MEDIA_ROOT = '/static/media/'

STATICFILES_DIRS = [
     os.path.join(BASE_DIR, "static"),
]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Cloudinary and Sentry configuration

CLOUDINARY = {
    'cloud_name': 'dvrrqjzay',
    'api_key': '587771642844978',
    'api_secret': os.getenv('CLOUDINARY_API_SECRET', False) or 'this is not a relevant secret'
}

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = os.getenv('HOSTNAME')
EMAIL_HOST = '127.0.0.1'
#EMAIL_PORT = 587
EMAIL_PORT = 25
#EMAIL_HOST_USER = os.getenv('USERNAME
EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')
EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
EMAIL_USE_TLS = False
PASSWORD_RESET_PERIOD_IN_HOURS = 48
#DOMAIN_FOR_EMAILS = "http://refugive.com"
DOMAIN_FOR_EMAILS = "https://s55969da3.adsl.online.nl"
#DEFAULT_FROM_EMAIL = 'Maaike and Jasper from refugive <noreply@refugive.com>'
DEFAULT_FROM_EMAIL = 'Xuyi from refugive <noreply@s55969da3.adsl.online.nl>'
