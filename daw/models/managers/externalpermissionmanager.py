from daw import PERMISSION_EXTERNAL_CODE_NAME

from daw.models.managers.basemanager import BaseModelManager


__author__ = 'ahmetdal'


class ExternalPermissionManager(BaseModelManager):
    def get_queryset(self):
        return super(ExternalPermissionManager, self).get_queryset().filter(codename=PERMISSION_EXTERNAL_CODE_NAME)