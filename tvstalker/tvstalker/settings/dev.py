from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
#MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
#MEDIA_URL = '/media/'
#STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
#STATIC_URL = '/static/'

#WSGI_APPLICATION = 'tvstalker.wsgi.application'

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_tv',
        'USER': 'django_dev',
        'PASSWORD': 'django',
    }
}

SECRET_KEY = 'qwertyuiop'

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
