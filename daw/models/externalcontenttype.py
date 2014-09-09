from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from daw.models.managers.externalcontenttypemanager import ExternalContentTypeManager


__author__ = 'ahmetdal'


class ExternalContentType(ContentType):
    class Meta:
        verbose_name = _("Content Type")
        verbose_name_plural = _("Content Types")
        app_label = 'daw'
        proxy = True


    objects = ExternalContentTypeManager()






