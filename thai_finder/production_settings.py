import dj_database_url

ALLOWED_HOSTS = ['thai-finder.herokuapp.com']
DATABASES = {
    'default': dj_database_url.config()
}
