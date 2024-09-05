"""
Django settings for bwenge project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from datetime import timedelta
import environ
import os
from pathlib import Path

env = environ.Env(
    
    DEBUG=(bool, True)
)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['admin.bwenge.com','localhost','127.0.0.1','bwenge.com']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',
    "core",
    "corsheaders",
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',
    'dashpanel',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bwenge.urls'
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://admin.bwenge.com",
    "https://bwenge.com",
]

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

WSGI_APPLICATION = 'bwenge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'bwenge_database/db.sqlite3'),
    }
}


REST_FRAMEWORK={
    'NON_FIELD_ERRORS_KEY':'error',
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL="accounts.User"

APPEND_SLASH = False

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

OOGLE_CLIENT_ID=env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=env("GOOGLE_CLIENT_SECRET")
GITHUB_SECRET=env("GITHUB_SECRET")
GITHUB_CLIENT_ID=env("GITHUB_CLIENT_ID")
SOCIAL_AUTH_PASSWORD=env('SOCIAL_AUTH_PASSWORD')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Directory where Django will look for additional static files, aside from each app's 'static' directory
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'assets'),  # Change this to a different folder from STATIC_ROOT
    # os.path.join(BASE_DIR, 'static'),
)

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# Directory where the static files will be collected to
STATIC_ROOT = '/var/www/bwenge/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Good for production

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'  # Make sure to also set MEDIA_URL


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER = 'a7ec6b1ccc72cb'
# EMAIL_HOST_PASSWORD = '56d5f948f93624'
# DEFAULT_FROM_EMAIL='niyannick120@gmail.com'
# EMAIL_PORT = '2525'
# EMAIL_USE_TLS=True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bwengeorg@gmail.com'
EMAIL_HOST_PASSWORD = 'uvmy fodq jycu inhn' 
#orsu rfjj cyuk cmdq # Use an App password if 2FA is enabled
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'bwengeorg@gmail.com'



JAZZMIN_SETTINGS = {
    "site_title": "BWENGE ADMIN",
    "site_header": "BWENGE",
    "site_brand": "BWENGE",
    "site_logo": "/image/logo1.png",
    "login_logo": None,
    "copyright": "BWENGE R.L Ltd",

    }
