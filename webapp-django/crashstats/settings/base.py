# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'crashstats'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = list(INSTALLED_APPS) + [
    # Application base, containing global templates.
    '%s.base' % PROJECT_MODULE,
    # Example code. Can (and should) be removed for actual projects.
    '%s.crashstats' % PROJECT_MODULE,
    '%s.api' % PROJECT_MODULE,
    '%s.manage' % PROJECT_MODULE,
    '%s.supersearch' % PROJECT_MODULE,
    'jingo_offline_compressor',
    '%s.auth' % PROJECT_MODULE,
    'django_statsd',
    'django.contrib.messages',
    'raven.contrib.django.raven_compat',
    'waffle',
]


# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

MIDDLEWARE_EXCLUDE_CLASSES = [
    'funfactory.middleware.LocaleURLMiddleware',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)

for app in MIDDLEWARE_EXCLUDE_CLASSES:
    if app in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES.remove(app)

MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES) + (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'crashstats.crashstats.middleware.AnalyticsMiddleware',
    'waffle.middleware.WaffleMiddleware',
)


STATSD_CLIENT = 'django_statsd.clients.normal'


# BrowserID configuration
AUTHENTICATION_BACKENDS = [
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATE_CONTEXT_PROCESSORS += (
    'django_browserid.context_processors.browserid_form',
    'django.core.context_processors.request',
)

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.crashstats.db',
    }
}

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
],

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = dict(loggers=dict(playdoh={'level': logging.DEBUG}))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # fox2mike suggest to use IP instead of localhost
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 500,
        'KEY_PREFIX': 'crashstats',
    }
}

# Middleware related stuff
CACHE_MIDDLEWARE = True
CACHE_MIDDLEWARE_FILES = False  # store on filesystem instead of cache server

# Some products have a different name in bugzilla and Socorro.
BUG_PRODUCT_MAP = {
    'FennecAndroid': 'Firefox for Android',
    'B2G': 'Boot2Gecko',
}

# Link to source if possible
VCS_MAPPINGS = {
    'cvs': {
        'cvs.mozilla.org': ('http://bonsai.mozilla.org/cvsblame.cgi?'
                            'file=%(file)s&rev=%(revision)s&'
                            'mark=%(line)s#%(line)s')
    },
    'hg': {
        'hg.mozilla.org': ('http://hg.mozilla.org/%(repo)s'
                           '/annotate/%(revision)s/%(file)s#l%(line)s')
    },
    'git': {
        'git.mozilla.org': ('http://git.mozilla.org/?p=%(repo)s;a=blob;'
                            'f=%(file)s;h=%(revision)s#l%(line)s'),
        'github.com': ('https://github.com/%(repo)s/blob/%(revision)s/'
                       '%(file)s#L%(line)s')
    }
}

# top three operating systems
OPERATING_SYSTEMS = (
    'Linux',
    'Mac OS X',
    'Windows',
)

# Identifies nightly releases
NIGHTLY_RELEASE_TYPES = (
    'Aurora',
    'Nightly',
)


# by default, compression is done in runtime.
COMPRESS_OFFLINE = False

# True if old legacy URLs we handle should be permanent 301 redirects.
# Transitionally it might be safer to set this to False as we roll out the new
# django re-write of Socorro.
PERMANENT_LEGACY_REDIRECTS = True

# This is needed for BrowserID to work!
SITE_URL = 'http://localhost:8000'

LOGIN_URL = '/login/'
ALLOWED_PERSONA_EMAILS = (
    # fill this in in settings/local.py
)

# Use memcached for session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# we don't need bcrypt since we don't store real passwords
PWD_ALGORITHM = 'sha512'

# must be set but not applicable because we don't use bcrypt
HMAC_KEYS = {'any': 'thing'}

# Types of query that can be run in search
QUERY_TYPES = (
    'contains',
    'is_exactly',
    'starts_with',
    'simple',
    'exact',  # for backward compatibility
    'startswith',  # for backward compatibility
)

# This is for backward compatibility with the PHP app.
QUERY_TYPES_MAP = {
    'exact': 'is_exactly',
    'startswith': 'starts_with',
}

# Maximum and default range of query that can be run in search
QUERY_RANGE_MAXIMUM_DAYS = 30
QUERY_RANGE_MAXIMUM_DAYS_ADMIN = 120
QUERY_RANGE_DEFAULT_DAYS = 14

# range unit values to allow in queries
RANGE_UNITS = (
    'weeks',
    'days',
    'hours',
)

# process types to allow in queries
PROCESS_TYPES = (
    'any',
    'browser',
    'plugin',
    'content',
    'all',  # alias for 'any'
)

# hang types to allow in queries
HANG_TYPES = (
    'any',
    'crash',
    'hang',
    'all',  # alias for 'any'
)

# plugin fields to allow in queries
PLUGIN_FIELDS = (
    'filename',
    'name',
)

# this is the max length of signatures in forms
SIGNATURE_MAX_LENGTH = 255

# We use django.contrib.messages for login, so let's use SessionStorage
# to avoid byte-big messages as cookies
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# LDAP related settings
# feel free to override these in settings/local.py
LDAP_SERVER_URI = 'ldap://pm-ns.mozilla.org'
# search base where querys start
LDAP_SEARCH_BASE_USER = 'dc=mozilla'
LDAP_SEARCH_BASE_GROUP = 'ou=groups,dc=mozilla'
# groups you must belong to to be able log in
LDAP_GROUP_NAMES = ['CrashReportsAdmin']
# list of group queries that is intersected wih the `LDAP_GROUP_NAMES` search
LDAP_GROUP_QUERIES = [
    'mail=%(mail)s,o=com,dc=mozilla',
    'mail=%(mail)s,o=org,dc=mozilla',
    'mail=%(mail)s,o=net,dc=mozilla',
]


# A prefix that is sometimes prefixed on the crash ID when used elsewhere in
# the socorro eco-system.
CRASH_ID_PREFIX = 'bp-'


# If true, allow robots to spider the site
ENGAGE_ROBOTS = False


# Base URL for when we use the Bugzilla API
BZAPI_BASE_URL = 'https://api-dev.bugzilla.mozilla.org/1.3'

# Specify the middleware implementation to use in the middleware
# Leave empty to use the default
SEARCH_MIDDLEWARE_IMPL = None

# Valid type for correlations reports
CORRELATION_REPORT_TYPES = (
    'core-counts',
    'interesting-addons',
    'interesting-addons-with-versions',
    'interesting-modules',
    'interesting-modules-with-versions'
)

# Default number of crashes to show on the Exploitable Crashes report
EXPLOITABILITY_BATCH_SIZE = 250

# Default number of days to show in explosive crashes reports
EXPLOSIVE_REPORT_DAYS = 10
