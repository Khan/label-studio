"""This is a settings file intended for use when running the label studio app locally"""
from khan.settings.base import *

# For local, we want to be able to create users since we don't have IAP
DISABLE_SIGNUP_WITHOUT_LINK = False

# Unless set in the env, use DEBUG level logging for local runs
LOGGING['root']['level'] = get_env('LOG_LEVEL', 'DEBUG')

# Use sqlite for local
DATABASES = {'default': DATABASES_ALL[DJANGO_DB_SQLITE]}

# Unless set in the env, run in DEBUG mode
DEBUG = get_bool_env('DEBUG', True)
DEBUG_PROPAGATE_EXCEPTIONS = get_bool_env('DEBUG_PROPAGATE_EXCEPTIONS', True)
