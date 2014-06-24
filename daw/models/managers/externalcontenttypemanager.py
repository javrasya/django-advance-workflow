from django.conf import settings

from daw.models.managers.basemanager import BaseModelManager


__author__ = 'ahmetdal'


class ExternalContentTypeManager(BaseModelManager):
    def get_queryset(self):
        return super(ExternalContentTypeManager, self).get_queryset().filter(app_label=settings.CONTENT_TYPE_EXTERNAL_APP_LABEL)