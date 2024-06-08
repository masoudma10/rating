from .base import *


SECRET_KEY = 'django-insecure-7710xfbykyqi03rn%$!4^yjyge+q@@&$=d95emutdw2)a7)i46'
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rating',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.getenv('CACHE_KEY_PREFIX', 'rating'),
        "VERSION": 4,
    },

}

CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_DEFAULT_QUEUE = 'default'
CELERY_TIMEZONE = 'Asia/Tehran'
CELERY_VISIBILITY_TIMEOUT = 365*86400