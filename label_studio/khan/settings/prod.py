"""This is a settings file intended for use when running the label studio app in the production environment"""
from khan.settings.base import *

# make sure our IAP user middleware is present so we populate a user
# object on the request from the IAP jwt
MIDDLEWARE.append("khan.iap.middleware.IAPUserMiddleware")
