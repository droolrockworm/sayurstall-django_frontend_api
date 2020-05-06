"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

with open('/data/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()
# SECRET_KEY = 'u@=6y7y(sy)&sht@0ck*)jeomqj0f4(v@dnqyo1jx=(@7n&#hk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sayurstall.com','localhost', '0.0.0.0','18.136.95.78']

## For "Daily" database
MONGO_URL='mongodb://root:beetroot@db.unityesg.net/daily'
MONGO_HOST='db.unityesg.net'
MONGO_PORT = 27017
MONGO_DB='daily'
MONGO_URL1='mongodb://db.unityesg.net'


# MONGO_HOST='108.171.187.13'
# MONGO_DB='kl'
# MONGO_PW='un1ty'


LOGIN_URL = "login/"
LOGIN_REDIRECT_URL = "/"

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'locations',
    'test',
    # 'tz_detect',
    # 'easy_timezones',
]
# GEOIP_DATABASE = '/data/portal/portal/GeoLite2-City_20200414/GeoLite2-City.mmdb'
# GEOIP_DATABASE = '/data/portal/portal/GeoLite2-City_20200414/GeoLite2-City.mmdb'
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'tz_detect.middleware.TimezoneMiddleware',
    # 'easy_timezones.middleware.EasyTimezoneMiddleware',
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'portal.wsgi.application'


# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'newdjango',
#         'USER': 'root',
#         'PASSWORD': 'beetroot',
#         'HOST': 'db.unityesg.net',
#         'PORT': '3306'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sayur',
        'USER': 'root',
        'PASSWORD': 'beetroot',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}



EMAIL_HOST = 'mail.authsmtp.com'
EMAIL_PORT = 23
EMAIL_HOST_USER = 'ac53252'
EMAIL_HOST_PASSWORD = 'qxnmyww4hvrmhe'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Makassar'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),os.path.join(BASE_DIR, 'images'), ]

# MEDIA_ROOT = os.path.join(BASE_DIR, '/')
MEDIA_URL = '/images/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
