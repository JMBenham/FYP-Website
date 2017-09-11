from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['vast-gorge-31543.herokuapp.com']

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))