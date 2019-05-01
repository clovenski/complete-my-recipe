from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# CORS

CORS_ORIGIN_ALLOW_ALL = True

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

TEMPLATES[0]['DIRS'].append(os.path.join(PROJECT_DIR, 'static/'))
TEMPLATES[0]['DIRS'].append(os.path.join(PROJECT_DIR, 'templates/'))