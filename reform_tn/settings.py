# Django settings for reform_tn project.

import os
PROJECT_DIR=os.path.dirname(__file__)

DEBUG = True
#DEBUG = False # for production
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_DEBUG = False # for production

ADMINS = (
    ('Nader Toukabri', 'nader.toukabri@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'reform_tn/development.sqlite3', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        #'USER': '',
        #'PASSWORD': '',
        #'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', 'reform.tn', 'www.reform.tn']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Tunis'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'


LANGUAGES = (
	('en', 'English'),
	('fr', 'French'),
	('ar', 'Arabic'),
	('ar-tn', 'Tounsi'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


DATETIME_INPUT_FORMATS = (
	'%Y-%m-%dT%H:%M:%S',     # '2006-10-25T14:30:59'
	'%Y-%m-%dT%H:%M',        # '2006-10-25T14:30'
	'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
	'%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
	'%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
	'%Y-%m-%d',              # '2006-10-25'
	'%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
	'%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
	'%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
	'%m/%d/%Y',              # '10/25/2006'
	'%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
	'%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
	'%m/%d/%y %H:%M',        # '10/25/06 14:30'
	'%m/%d/%y',              # '10/25/06'
)


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR,'static/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g#t3tki%zbnynjn1qlkqn#jlulv9!w*=l0e_n7j^%mm7%5@jr%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'reform_tn.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'reform_tn.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'suit', # theme for admin
    'admin_theme',
    'django_admin_bootstrapped', # theme for admin
    'django.contrib.admin',
    #'django.contrib.admindocs',

    # project components
    'base',
    'reports',
    'categories',
    'features',
    'victims',

    # dev dependencies
    'debug_toolbar',

		# project dependencies
    'form_utils',
    'widget_tweaks',
    'floppyforms',
    'crispy_forms',

    'rest_framework',

    'jsonify',

		#'django_youtube',

)

#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

#TEMPLATE_CONTEXT_PROCESSORS = TCP + (
#    'django.core.context_processors.request',
#)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'default': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'reports': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

INTERNAL_IPS = ('127.0.0.1',)


REST_FRAMEWORK = {
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}



YOUTUBE_AUTH_EMAIL = 'yourmail@gmail.com'
YOUTUBE_AUTH_PASSWORD = 'yourpassword'
YOUTUBE_DEVELOPER_KEY = 'developer key, get one from http://code.google.com/apis/youtube/dashboard/'
YOUTUBE_CLIENT_ID = 'client-id'


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = -1
