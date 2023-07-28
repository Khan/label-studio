"""This is a settings file intended for use when running the label studio app in the test environment"""
# TODO(jimmy): do we even need this file? can we just use prod and configure from env vars instead?
from khan.settings.base import *

# make sure our IAP user middleware is present so we populate a user
# object on the request from the IAP jwt
MIDDLEWARE.append("khan.iap.middleware.IAPUserMiddleware")
