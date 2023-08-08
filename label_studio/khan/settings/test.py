"""This is a settings file intended for use when running the label studio app in the test environment"""
from khan.settings.base import *

# make sure our IAP user middleware is present so we populate a user
# object on the request from the IAP jwt
MIDDLEWARE.append("khan.iap.middleware.IAPUserMiddleware")

# Unless set in the env, use DEBUG level logging for local runs
LOGGING['root']['level'] = get_env('LOG_LEVEL', 'DEBUG')

# Unless set in the env, run in DEBUG mode
DEBUG = get_bool_env('DEBUG', True)
DEBUG_PROPAGATE_EXCEPTIONS = get_bool_env('DEBUG_PROPAGATE_EXCEPTIONS', True)
