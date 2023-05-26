from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'test_db'),
        'USER': os.getenv('POSTGRES_USER', 'test'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'testpass'),
        'HOST': os.getenv("DB_HOST", "postgresdb"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

# Redis settings
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 1