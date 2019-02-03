import dj_database_url
import os

from django.core.exceptions import ImproperlyConfigured


ALLOWED_HOSTS = ['thai-finder.herokuapp.com']
DATABASES = {
    'default': dj_database_url.config()
}
try:
    SECRET_KEY = os.environ.get('SECRET_KEY')
except KeyError:
    raise ImproperlyConfigured('Secret key environment variable required on production.')
