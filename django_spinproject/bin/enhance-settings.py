#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv

template = """
# Generated by 'django-spinproject', based on Django 2.1.2.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/2.1/topics/settings/
#
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/2.1/ref/settings/
#
# Production use checklist:
# https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

import environ
env = environ.Env(
	DJANGO_DEBUG=(bool, False),  # casting, default value
	DJANGO_DEBUG_SQL=(bool, False),
)
environ.Env.read_env()

def passthrough(x):
	# print('passthrough', repr(x))
	return x

import os

SECRET_KEY = passthrough(env('DJANGO_SECRET_KEY'))
DEBUG = passthrough(env('DJANGO_DEBUG'))
ALLOWED_HOSTS = passthrough(env.list('DJANGO_ALLOWED_HOSTS'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

def readonly(x):
	x['ENGINE'] = '"""+name+""".pg_readonly'
	return x

DATABASES = {
	'default': passthrough(env.db('DJANGO_DATABASE_URL')),
	#'additional': passthrough(readonly(env.db('DJANGO_DATABASE_ADDITIONAL_URL'))),
}


# Application definition

INSTALLED_APPS = [
	'whitenoise.runserver_nostatic',

	# place your apps here

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',

	'whitenoise.middleware.WhiteNoiseMiddleware',

	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '"""+name+""".urls'

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
			],
		},
	},
]

WSGI_APPLICATION = '"""+name+""".wsgi.application'
# ASGI_APPLICATION = '"""+name+""".asgi.application'  # uncomment if needed


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{ 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
	{ 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
	{ 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
	{ 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'stamp': {
			'format': '%(asctime)s %(name)s %(module)s [%(levelname)s] %(message)s'
		},
	},
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'stamp',
		},
	},
	'loggers': {
		# 'django': {
		# 	'handlers': ['console'],
		# 	'level': 'DEBUG',
		# },
		'"""+name+"""': {
			'handlers': ['console'],
			'level': 'DEBUG',
		},
	},
}
if env('DJANGO_DEBUG_SQL'):
	LOGGING['loggers']['django.db'] = {
		'handlers': ['console'],
		'level': 'DEBUG',
	}


## No-CSRF auth is required for xauth

# from rest_framework.authentication import SessionAuthentication
# class CsrfExemptSessionAuthentication(SessionAuthentication):
# 	def enforce_csrf(self, request):
# 		# Ignore CSRF checks (that's a security hole, make sure you know what you're doing)
# 		return
#
# REST_FRAMEWORK = {
# 	'DEFAULT_PERMISSION_CLASSES': [
# 		'rest_framework.permissions.IsAuthenticated',
# 	],
# 	'DEFAULT_AUTHENTICATION_CLASSES': [
# 		'"""+name+""".settings.CsrfExemptSessionAuthentication',
# 		# 'rest_framework.authentication.SessionAuthentication',
# 		'rest_framework.authentication.BasicAuthentication',
# 	],
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

## Whitenoise

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
"""

print('Saving original settings as .orig...')
subprocess.run(['mv', os.path.join(path, name, 'settings.py'), os.path.join(path, name, 'settings.py.orig')], check=True)

print('Writing new settings.py...')
with open(os.path.join(path, name, 'settings.py'), 'w') as f:
	f.write(template)

# .env files
template = f'''DJANGO_SECRET_KEY=""
DJANGO_DEBUG=True
DJANGO_DEBUG_SQL=False
DJANGO_ALLOWED_HOSTS=""
DJANGO_DATABASE_URL="sqlite:///db.sqlite3"'''
for filename in ['.env.example']:
	with open(os.path.join(path, name, filename), 'w') as f:
		print(f'Writing {filename}...')
		f.write(template)


print(f"""---
Note: manual installation of third-party packages is required.
These commands should do the trick:

 cd "{path}"
 poetry init
 poetry add django
 poetry add django-environ whitenoise
 poetry add --dev flake8
 # Also, if you intend to use PostgreSQL
 poetry add psycopg2-binary

If you don't use poetry, other package manager will do, too.
---""")
