from typing import Dict, Set

from django.db import models

from core.permissions import all_permissions


class Role(models.IntegerChoices):
    LABELER = 1
    LABELING_COORDINATOR = 2
    LABELING_INFRA = 3

    def has_perm(self, perm):
        return perm in _roles[self]


_roles: Dict[Role, Set[str]] = {}

_roles[Role.LABELER] = {
    all_permissions.organizations_view,
    all_permissions.projects_view,
    all_permissions.tasks_view,
    all_permissions.tasks_change,
    all_permissions.annotations_create,
    all_permissions.annotations_view,
    all_permissions.annotations_change,
    all_permissions.annotations_delete,
    all_permissions.actions_perform,
    all_permissions.predictions_any,
    all_permissions.avatar_any,
    all_permissions.labels_create,
    all_permissions.labels_view,
    all_permissions.labels_change,
    all_permissions.labels_delete,
}

_roles[Role.LABELING_COORDINATOR] = _roles[Role.LABELER] | {
    all_permissions.projects_create,
    all_permissions.projects_change,
    all_permissions.projects_delete,
    all_permissions.tasks_create,
    all_permissions.tasks_delete,
}

_roles[Role.LABELING_INFRA] = _roles[Role.LABELING_COORDINATOR] | {
    all_permissions.organizations_create,
    all_permissions.organizations_change,
    all_permissions.organizations_delete,
    all_permissions.organizations_invite,
}
