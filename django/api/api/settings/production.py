from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1' ,'localhost', 'completemyrecipe.pythonanywhere.com']

CORS_ORIGIN_WHITELIST = ['127.0.0.1:8000' , 'localhost:8000', 'completemyrecipe.pythonanywhere.com']

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'