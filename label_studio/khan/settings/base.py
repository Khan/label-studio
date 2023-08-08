"""This is the settings file that serves as the base for all other khan run environments.
It inherits from the label-studio core base settings, and all khan's settings files should inherit from this.
"""
from core.settings.base import *

# Make sure our custom django app is installed
INSTALLED_APPS.extend([
    "khan",
    "khan.rbac"
])

# Add our Rules Permissions Class to drf permissions classes so our
# custom RBAC works
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'].append(
    "khan.rbac.permission.RBACPermissionClass"
)

# Default Logging to INFO level
LOGGING['root']['level'] = get_env('LOG_LEVEL', 'INFO')

# Default to PSQL
DATABASES = {'default': DATABASES_ALL[DJANGO_DB_POSTGRESQL]}

# IAP _should_ mean users never even see the login page, but on the off chance they do,
# they shouldn't be able to create their own user accounts
DISABLE_SIGNUP_WITHOUT_LINK = True

# IAP Audience used for IAP JWT validation
IAP_AUDIENCE = get_env("IAP_AUDIENCE")

# Don't send telemetry data to tele.labelstud.io
COLLECT_ANALYTICS = False

# Not sure if things below this line are needed, they came from the label-studio/settings/label-studio file
MIDDLEWARE.append('organizations.middleware.DummyGetSessionMiddleware')
MIDDLEWARE.append('core.middleware.UpdateLastActivityMiddleware')
if INACTIVITY_SESSION_TIMEOUT_ENABLED:
    MIDDLEWARE.append('core.middleware.InactivitySessionTimeoutMiddleWare')

ADD_DEFAULT_ML_BACKENDS = False

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

RQ_QUEUES = {}

# in Label Studio Community version, feature flags are always ON
FEATURE_FLAGS_DEFAULT_VALUE = True

STORAGE_PERSISTENCE = get_bool_env('STORAGE_PERSISTENCE', True)
