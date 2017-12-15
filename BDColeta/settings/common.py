"""
Common Django settings for the BDColeta project.

See the local, test, and production settings modules for the values used
in each environment.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','86u#+a)d=r%1g-*@lk3d=%m5($+9wz@le(c@c*7j&7$cz3dic7')

# Most important settings


ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'bootstrap3',
    'django_forms_bootstrap',
    'timezone_field',
    'widget_tweaks',
    'crispy_forms',
    'django_addanother',
    'guardian',
    'geoposition',
    'import_export',
)

LOCAL_APPS = (
    'peixes',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'BDColeta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
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


CRISPY_TEMPLATE_PACK = 'bootstrap3'

WSGI_APPLICATION = 'BDColeta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'BDColeta_v7',
        'USER': 'postgres',
        'PASSWORD': 'yecopostgresql',
        'CONN_MAX_AGE': 60,
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = BASE_DIR + '/static'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

#STATICFILES_DIRS = [os.path.join(BASE_DIR, '/peixes/static_own')]


#Redirect after login
LOGIN_REDIRECT_URL = '/'

#EMAIL BACKEND AND CONFIGURATIONS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.mailgun.org'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'postmaster@ns01.freenom.com'
# EMAIL_HOST_PASSWORD = 'yecofreenom23'
# EMAIL_USE_TLS = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'BDColeta@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'BDColeta Admin'

#DJANGO REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 7

#GOOGLE API KEY FOR GOOGLE MAPS

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyAbD6RLKgEI_Vk0BzhEcZ3USq4pN3_nPak'

GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}

#CONFIGURATION FOR IMPORT AND EXPORT
IMPORT_EXPORT_USE_TRANSACTIONS = True
