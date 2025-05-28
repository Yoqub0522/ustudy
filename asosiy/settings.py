
from pathlib import Path

from django.conf.global_settings import MEDIA_ROOT
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lz0sexi(viu(@gj4hpefb3$^i^h+(hg-ct@c0z^klu+%99lxlg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

import os
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['.onrender.com']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'new',
    'user',
    'widget_tweaks',
    'captcha',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user.middleware.LoginMiddleware',
    'user.middleware.RateLimitMiddleware',
    'crum.CurrentRequestUserMiddleware',

]

ROOT_URLCONF = 'asosiy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'asosiy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'django_project',             # PostgreSQL bazangiz nomi
#         'USER': 'postgres',           # PostgreSQL foydalanuvchi nomi
#         'PASSWORD': 'Yoqub0522',   # Parolingiz
#         'HOST': 'localhost',        # Yoki masofaviy host
#         'PORT': '5432',             # Standart PostgreSQL porti
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#claud

import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://neondb_owner:npg_mKqIx7wAuVZ4@ep-calm-snow-a491d1ql-pooler.us-east-1.aws.neon.tech/baza',
        conn_max_age=600,
        ssl_require=True
    )
}






# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT=BASE_DIR/'media'
MEDIA_URL='/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'course-list'
LOGOUT_REDIRECT_URL = '/login/'
AUTH_USER_MODEL = 'user.CustomUser'



STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = "axmedov.yoqub0522@gmail.com"

EMAIL_HOST_PASSWORD = "dsao pkxy bwjg akyo"

# settings.py

from user.signalbot import TelegramHandler  # yuqoriga qo‘shing

TELEGRAM_TOKEN = '7682205826:AAHhi1hZNVmJqaq6zD7-gf_phaPzdxvOxwc'
TELEGRAM_CHAT_ID = 858267509

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'telegram': {
            'format': '[{asctime}] {levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'telegram_info': {
            'level': 'INFO',
            'class': 'user.signalbot.TelegramHandler',
            'formatter': 'telegram',
            'token': TELEGRAM_TOKEN,
            'chat_id': TELEGRAM_CHAT_ID,
        },
        'telegram_warning': {
            'level': 'WARNING',
            'class': 'user.signalbot.TelegramHandler',
            'formatter': 'telegram',
            'token': TELEGRAM_TOKEN,
            'chat_id': TELEGRAM_CHAT_ID,
        },
        'telegram_error': {
            'level': 'ERROR',
            'class': 'user.signalbot.TelegramHandler',
            'formatter': 'telegram',
            'token': TELEGRAM_TOKEN,
            'chat_id': TELEGRAM_CHAT_ID,
        },
    },

    'loggers': {
        'telegram': {
            'handlers': ['telegram_info', 'telegram_warning', 'telegram_error'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
# gogle avtorizatsiya
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))  # yoki 'asosiy/.env' bo‘lsa shunga mos yo‘l

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

GOOGLE_AUTH_URL = os.getenv('GOOGLE_AUTH_URL')

GOOGLE_USER_INFO_URL =os.getenv('GOOGLE_USER_INFO_URL')

GOOGLE_TOKEN_URL =os.getenv('GOOGLE_TOKEN_URL')
