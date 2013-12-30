# Django settings for reporto project.

import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# DEBUG = True # !DEV!
DEBUG = False  # !PROD!
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Administrator', 'admin@reform.tn'),
    ('Nader Toukabri', 'nader.toukabri@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reporto',
        'USER': 'reporto',
        'PASSWORD': 'reportopass',
    }
}

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'reporto'
EMAIL_HOST_PASSWORD = 'reportopass'
DEFAULT_FROM_EMAIL = 'contact@reform.tn'
SERVER_EMAIL = 'contact@reform.tn'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ['localhost', 'nader-laptop.local', 'reform.tn', 'www.reform.tn', 'tunpixel.webfactional.com', 'reporting.reform.tn', 'reform-tn-platform.herokuapp.com']
ALLOWED_HOSTS = ['*']
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    #('ar-tn', 'Tounsi'),
)

SITE_ID = 3

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


# DATETIME_INPUT_FORMATS = (
# '%Y-%m-%dT%H:%M:%S',     # '2006-10-25T14:30:59'
# '%Y-%m-%dT%H:%M',        # '2006-10-25T14:30'
# '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
# '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
# '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
# '%Y-%m-%d',              # '2006-10-25'
# '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
# '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
# '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
# '%m/%d/%Y',              # '10/25/2006'
# '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
# '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
# '%m/%d/%y %H:%M',        # '10/25/06 14:30'
# '%m/%d/%y',              # '10/25/06'
# )


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
#STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_DIR, '../staticfiles'),
    #os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g#t3tki%zbnynjn1qlkqn#jlulv9!w*=l0e_n7j^%mm7%5@jr%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'base.utils.template.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # !debug_toolbar!
)

ROOT_URLCONF = 'reporto.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'reporto.wsgi_production.application'

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
    #'django.contrib.markup',

    'reversion',
    'mptt',
    'watson',

    # project components
    'users',

    # admin components
    'admin_mod',
    'report_builder',
    #'filebrowser',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',  # theme for admin
    # 'suit',
    #'grappelli',
    'django.contrib.admin',
    #'django.contrib.admindocs',

    # project components
    'base',
    'violations',
    'violations_categories',
    'violations_features',
    'violations_victims',
    'appreciations',
    'appreciations_categories',

    # project dependencies
    'form_utils',
    'widget_tweaks',
    'floppyforms',
    'crispy_forms',
    'south',
    'compressor',
    'easy_thumbnails',
    'social_auth',

    # dev dependencies
    #'debug_toolbar',


)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = -1

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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
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
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'violations': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'appreciations': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

AUTH_USER_MODEL = 'users.User'

# APP 'debug_toolbar' !DEV!
INTERNAL_IPS = ('127.0.0.1', '127.0.1.1')
# DEBUG_TOOLBAR_CONFIG = {
#   'INTERCEPT_REDIRECTS': False
# }

# APP 'compressor'
#COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
    #'compressor.filters.yui.YUICSSFilter'
]
COMPRESS_JS_FILTERS = [
    # 'compressor.filters.jsmin.JSMinFilter',
    # 'compressor.filters.jsmin.SlimItFilter',
    # 'compressor.filters.yui.YUIJSFilter',
    # 'compressor.filters.closure.ClosureCompilerFilter',
]
COMPRESS_CLOSURE_COMPILER_BINARY = 'java -jar closure-compiler.jar'
COMPRESS_YUI_BINARY = 'java -jar yuicompressor.jar'

# APP 'easy_thumbnails'
THUMBNAIL_ALIASES = {
    '': {
        'media': {'size': (200, 150), 'crop': True, 'quality': 100},
        'report_comment': {'size': (150, 150), 'crop': False, 'quality': 100},
    },
}

# APP 'social_auth'
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.browserid.BrowserIDBackend',
    #'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)
TWITTER_CONSUMER_KEY = '3JUk9ltCW3UsEjeBdfFsg'
TWITTER_CONSUMER_SECRET = 'cm1fwhYAAIqkVOqPsMPTC5cGDDpDNSimHmLzrd753dU'
FACEBOOK_APP_ID = '365981540199699'
FACEBOOK_API_SECRET = '0582b7411bd999db01e6c739d93451bd'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# GOOGLE_CONSUMER_KEY          = ''
# GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID = '1083020802599.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'H4S_8BHCGsEbx5maus_9oZFe'
# YAHOO_CONSUMER_KEY           = ''
# YAHOO_CONSUMER_SECRET        = ''

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
#LOGIN_ERROR_URL    = '/login'


SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PROTECTED_USER_FIELDS = [
    'email', 'username', 'first_name', 'last_name']
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['next', ]

#SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    # 'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    #'users.pipeline.get_user',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)


# APP 'crispy_forms'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# APP 'report_builder'
#REPORT_BUILDER_INCLUDE = []
REPORT_BUILDER_EXCLUDE = ['user']
REPORT_BUILDER_GLOBAL_EXPORT = True
