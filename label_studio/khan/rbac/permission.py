import logging
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class RBACPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if isinstance(view.permission_required, str):
            perm = view.permission_required
        else:
            perm = getattr(view.permission_required, request.method, None)

        if perm is None:
            logger.warning(
                "path: %s method: %s has no perms",
                request.path,
                request.method,
            )
            return False

        try:
            return request.user.role.has_perm(perm)
        except ObjectDoesNotExist:
            # the user does not have a valid role assigned - default to no access
            logger.error("user %s has no role assigned", request.user.email)
            return False
