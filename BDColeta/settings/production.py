'''
Production settings

- Set secret key from environment variable
'''

from .common import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Allow all hosts, so we can run on PaaS's like Heroku
ALLOWED_HOSTS = ['bdcoleta.herokuapp.com','bdcoleta.com']

# Configure the production database using dj_database_url
import dj_database_url
db_from_env = dj_database_url.config()
#ESTO ES UNA PRUEBA
DATABASES['default'].update(db_from_env)

#STATIC FILES CONFIG
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Address of RedisToGo instance
BROKER_URL = os.environ.get('REDISTOGO_URL')

#GO LIVE SETTINGS 
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1000000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
