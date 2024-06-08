from .base import *


SECRET_KEY = os.environ.get('GENERAL_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


CELERY_BROKER_URL = f'amqp://{os.environ.get("USERNAME_RABBITMQ")}:{os.environ.get("PASSWORD_RABBITMQ")}@rabbitmq:5672//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'json'
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_DEFAULT_QUEUE = 'default'
CELERY_TIMEZONE = 'Asia/Tehran'
CELERY_VISIBILITY_TIMEOUT = 365*86400

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            f'redis://{os.environ.get("CACHE_ADDRESS1")}',  # leader
            f'redis://{os.environ.get("CACHE_ADDRESS2")}',  # read-replica 1
            f'redis://{os.environ.get("CACHE_ADDRESS3")}',  # read-replica 2
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.getenv('CACHE_KEY_PREFIX', 'rating'),
        "VERSION": 4,
    },

}
