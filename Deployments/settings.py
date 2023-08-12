"""
Django settings for flexydial project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from datetime import timedelta
import os
import socket
import pickle, redis, re
import uuid

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#globel variable for reusefull purpose.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*^gyxflla@kwhnj6$o)n=ihi2-ntcy-)t7phnc^%p!9_a&al&!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DEVELOPMENT = os.environ.get("DEVELOPMENT",False)
LOGIN_URL = '/'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'crm',
    'callcenter',
    'dialer',
    'scripts',
    'django_apscheduler',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'storages',
    'captcha',
    # 'debug_toolbar',
    "rest_framework.authtoken",
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'flexydial.session_middleware.SessionIdleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'flexydial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
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

WSGI_APPLICATION = 'flexydial.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('FLEXYDIAL_DB_NAME','flexydial'),
        'USER': os.environ.get('FLEXYDIAL_DB_USER','flexydial'),
        'PASSWORD': os.environ.get('FLEXYDIAL_DB_PASS',''),
        'HOST': os.environ.get('FLEXYDIAL_DB_HOST','127.0.0.1'),
        'PORT': os.environ.get('FLEXYDIAL_DB_PORT',5432),
    },
    'crm': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('CRM_DB_NAME','crm'),
        'USER': os.environ.get('CRM_DB_USER','flexydial'),
        'PASSWORD': os.environ.get('CRM_DB_PASS',''),
        'HOST': os.environ.get('CRM_DB_HOST','127.0.0.1'),
        'PORT': os.environ.get('CRM_DB_PORT',5432),
    },
}
DATABASE_ROUTERS = ['crm.router.DbRouter','callcenter.router.DbRouter']

PSQL_DB = DATABASES['default']

# Using connection string for Autodial SQLAlchemyJobStore
DB_CSTRING = {
    'default': 'postgres://%s:%s@%s/%s' % (
        PSQL_DB['USER'], PSQL_DB['PASSWORD'], PSQL_DB['HOST'], PSQL_DB['NAME'])
    }


# Redis settings starts
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/1" % ( os.environ.get('REDIS_HOST','127.0.0.1'),os.environ.get('REDIS_PORT',6379)),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

CACHE_TTL = 60 * 15
#Redis settings ends

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

#rest_framework permissions
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'scripts.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'scripts.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'scripts.pagination.DatatablesPageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

##Variable not in use
NODEJS_SOCKET_PORT = 3232
WEB_LIVE_STATUS_CHANNEL = 'flexydial-dashboard'

AUTH_USER_MODEL         = 'callcenter.User'
# MEDIA_ROOT              = os.path.join('/var/lib/flexydial/', 'media')
MEDIA_ROOT              = 'media'
# MEDIA_URL               = '/media/'
RECORDING_ROOT          = '/var/spool/freeswitch/default'
RECORDING_URL           = '/recordings/'
RPC_HOST                = 'localhost'
RPC_USERNAME            = 'freeswitch'
RPC_PASSWORD            = 'works'
RPC_PORT                = '8080'
R_SERVER                = redis.Redis(connection_pool=redis.ConnectionPool(
                            host=os.environ.get('REDIS_HOST'),port=os.environ.get('REDIS_PORT'),db=0))
NDNC_URL                = 'http://127.0.0.1:5000/search/%s'
FS_ORIGINATE            = \
        "expand originate "\
        "{ignore_early_media=true,campaign='$campaign_slug',"\
        "phonebook='$phonebook_id',contact_id='$contact_id',$variables}$dial_string $campaign_extension"
# FS_MANUAL_ORIGINATE     = \
#         "{$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

FS_WFH_PROGRESSIVE_ORIGINATE     = \
        "{$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

FS_MANUAL_ORIGINATE     = "originate {$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

###### To reload all static data to client ######
URL_PARAMETER = str(uuid.uuid4())

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = '/etc/apache2/sites-available/flexydial.com/'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADDRESS = s.getsockname()[0]
s.close()
INTERNAL_IPS = [IP_ADDRESS, "127.0.0.1"]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_IDLE_TIMEOUT = 240*60  # 4 hours
SESSION_COOKIE_AGE = 540*60    # 9 hours
# resetting the password url valid days
PASSWORD_RESET_TIMEOUT_DAYS = 1

WEB_SOCKET_HOST = os.environ.get('WEB_SOCKET_HOST',"")
FREESWITCH_IP_ADDRESS = os.environ.get('FREESWITCH_HOST',"")
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME',"")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = os.environ.get('AWS_S3_OBJECT_PARAMETERS',{'CacheControl': 'max-age=86400'})
AWS_DEFAULT_ACL = os.environ.get("AWS_DEFAULT_ACL","")
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID',"")
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY',"")

GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME","")
JSON_KEY = {}
if JSON_KEY:
    from google.oauth2 import service_account
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(JSON_KEY)
    GS_DEFAULT_ACL = None
    GS_EXPIRATION = timedelta(seconds=86400)
if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'flexydial.storages.MediaStore'
elif GS_BUCKET_NAME:
    MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)
    DEFAULT_FILE_STORAGE='flexydial.storages.GoogleCloudMediaFileStorage'
    # STATICFILES_STORAGE = 'flexydial.storages.staticGCloudMedia'

API_CAMPAIGN_FIELD = os.environ.get('API_CAMPAIGN_FIELD',"campaign")
API_NUMERIC_FIELD = os.environ.get('API_NUMERIC_FIELD',"numeric")
REPLACE_API_KEY = os.environ.get('REPLACE_API_KEY',"")
REPLACE_API_VALUE = os.environ.get('REPLACE_API_VALUE',"")
XML_INSERT_KEY = os.environ.get("XML_INSERT_KEY","")
XML_UPDATE_KEY = os.environ.get("XML_UPDATE_KEY","")
API_DEST_CAMP = os.environ.get('API_DEST_CAMP','')
S3_GCLOUD_BUCKET_NAME = os.environ.get("S3_GCLOUD_BUCKET_NAME","")
DATA_UPLOAD_MAX_NUMBER_FIELDS = os.environ.get('DATA_UPLOAD_MAX_NUMBER_FIELDS',1500)
FS_INTERNAL_IP = os.environ.get('FS_INTERNAL_IP',FREESWITCH_IP_ADDRESS)

SOURCE = 'FLEXY'
LOCATION = 'Mumbai'

SSL_CERTIFICATE = "/etc/ssl/ca-flexydial.crt"
# def show_toolbar(request):
#     return True
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
# }
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

SERVICES_LIST= []

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
REDIS_KEY_EXPIRE_IN_SEC = os.environ.get('REDIS_KEY_EXPIRE_IN_SEC',32400)
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST",'localhost')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[Flexydial-Log] %(levelname)s %(asctime)s %(module)s '
                      '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}