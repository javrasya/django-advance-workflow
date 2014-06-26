from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from daw.models.managers.externalpermissionmanager import ExternalPermissionManager


__author__ = 'ahmetdal'


class ExternalPermission(Permission):
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permission")
        proxy = True


    objects = ExternalPermissionManager()






