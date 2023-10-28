"""
Django settings for browsedocs project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import environ
import dj_database_url
from email.headerregistry import Address
from google.oauth2 import service_account


from pathlib import Path

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = bool(int(env('DEBUG')))


if DEBUG:
    SECRET_KEY = env.get_value('SECRET_KEY', default='django-insecure-ksg!i&r49#t+x6*f^v#glkvhg_nfb^24r%l7im#ti-(it!5(y6')

else:
    SECRET_KEY = env.get_value('PORD_SECRET_KEY')

if DEBUG:
    ALLOWED_HOSTS = []

else:
    ALLOWED_HOSTS = env('ALLOWED_PROD_HOSTS').replace(' ', '').split(',')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'tailwind',
    'theme',
    'corsheaders',
    'django_celery_beat',
    'django_browser_reload',

]


LOGIN_URL = '/user/login/'

AUTH_USER_MODEL = "user.User" 

TAILWIND_APP_NAME = 'theme'

RATELIMIT_VIEW = 'browsedocs.views.rate_limiter_view'

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

else: 
    CELERY_BROKER_URL = env('REDIS_PROD_HOST')


CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_IMPORTS = ['utils.tasks',]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware', #whitenoise

    'django_browser_reload.middleware.BrowserReloadMiddleware', # reload
    
    'django_ratelimit.middleware.RatelimitMiddleware',
    'browsedocs.middlewares.RateLimitJsonResponseMiddleware',
  
    'browsedocs.middlewares.FileUploadMiddleware',

]

ROOT_URLCONF = 'browsedocs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'browsedocs.context_processors.secrets',

            ],
        },
    },
]

WSGI_APPLICATION = 'browsedocs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR.joinpath("templates"),
]


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles', 'static')
STATICFILES_DIRS = [
                        BASE_DIR.joinpath('templates'),
                        BASE_DIR.joinpath('templates', 'js'),
                        BASE_DIR.joinpath('templates', 'css'),
                        BASE_DIR.joinpath('templates', 'assets'),
                    ]

MEDIA_ROOT = BASE_DIR.joinpath('media')

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_DOMAIN = 'http://localhost:8000'
   
else:
    MEDIA_URL = '/media/'

    # Define the storage settings for media files
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_BUCKET_NAME = env("BUCKET_NAME")
    GS_PROJECT_ID = env("PROJECT_ID")
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        BASE_DIR.joinpath(env("FIREBASE_CRED_PATH"))
    )
    GS_DEFAULT_ACL = "publicRead"  # Optional: Set ACL for public access
    GS_QUERYSTRING_AUTH = True  # Optional: Enable querystring authentication
    GS_FILE_OVERWRITE = False # prevent overwriting


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

        # Send info messages to syslog
        # 'syslog':{
        #     'level':'INFO',
        #     'class': 'logging.handlers.SysLogHandler',
        #     'facility': SysLogHandler.LOG_LOCAL2,
        #     'address': '/dev/log',
        #     'formatter': 'verbose',
        # },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # critical errors are logged to sentry
        # 'sentry': {
        #     'level': 'ERROR',
        #     'filters': ['require_debug_false'],
        #     'class': 'raven.contrib.django.handlers.SentryHandler',
        # },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'mail_admins', 'celery'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}