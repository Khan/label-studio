import logging
from time import time
from typing import Dict, Optional

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests

from organizations.models import Organization


logger = logging.getLogger(__name__)

User = auth.get_user_model()

IAP_AUDIENCE = getattr(settings, "IAP_AUDIENCE", None)
IAP_HEADER = getattr(settings, "IAP_HEADER", "x-goog-iap-jwt-assertion")
IAP_CERT_URL = getattr(
    settings,
    "IAP_CERT_URL",
    "https://www.gstatic.com/iap/verify/public_key"
)


def _create_user(email):
    """Create a new user with the provided email as username and email.
    If an organization already exists, assign the new user to it, otherwise create
    a new org created by the user.
    """
    user = User.objects.create_user(email=email, username=email)
    user.set_unusable_password()

    if Organization.objects.exists():
        org = Organization.objects.first()
        org.add_user(user)
    else:
        org = Organization.create_organization(
            created_by=user, title='Label Studio')
    user.active_organization = org
    user.save(update_fields=['active_organization'])
    return user


def _decode_token(request) -> Optional[Dict]:
    """Decode the jwt assertion from the request header.
    If the token header is missing, or the token is invalid, returns None
    otherwise returns the decoded assertion as a Dict
    """
    logger.debug("decoding user from jwt")
    encoded_token = request.headers.get(IAP_HEADER)
    if encoded_token is None:
        logger.warn("no token provided in header")
        return None
    try:
        return id_token.verify_token(
            encoded_token,
            requests.Request(),
            audience=IAP_AUDIENCE,
            certs_url=IAP_CERT_URL,
        )
    except ValueError as e:
        logger.warn("invalid token: %s", e)
        return None


def _get_user(request):
    """Looks up a user object based on the email address present in the jwt assertion
    on the request header. If the token is missing or invalid, None is returned.
    If the email address does not belong to an existing user, a new one is created and
    returned.
    """
    token = _decode_token(request)
    if token is None:
        return None

    logger.debug("decoded token: %s", token)
    user = None
    if email := token.get("email"):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = _create_user(email)

    return user


def IAPUserMiddleware(get_response):
    """Middleware function that looks up or creates a user based on the IAP JWT assertion
    and then logs that user in.
    """
    def middleware(request):
        if not (request.user and request.user.is_authenticated):
            # if a user either doesn't exist on the request or isn't authenticated
            if (user := _get_user(request)) is not None:
                request.user = user
                request.session['last_login'] = time()
                auth.login(
                    request,
                    user,
                    backend='django.contrib.auth.backends.ModelBackend'
                )
        return get_response(request)
    return middleware
