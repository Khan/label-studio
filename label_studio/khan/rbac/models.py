from django.contrib.auth.models import auth
from django.db import models

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from khan.rbac.roles import Role

User = auth.get_user_model()


class UserRole(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="role",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    role = models.IntegerField(
        _("role"),
        default=Role.LABELER,
        choices=Role.choices,
    )

    def has_perm(self, perm: str) -> bool:
        return Role(self.role).has_perm(perm)

    def __str__(self) -> str:
        return self.user.email + " - " + Role(self.role).name


# on user save, if the user is being created, create a UserRole for them,
# with the default UserRole.role value
@receiver(post_save, sender=User)
def init_user(sender, instance=None, created=False, **kwargs):
    if created:
        UserRole.objects.create(user=instance)
