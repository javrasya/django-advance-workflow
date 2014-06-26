import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from daw import CONTENT_TYPE_EXTERNAL_APP_LABEL, PERMISSION_EXTERNAL_CODE_NAME

from daw.models.externalcontenttype import ExternalContentType
from daw.models.externalpermission import ExternalPermission
from daw.models.managers.externalcontenttypemanager import ExternalContentTypeManager


class ContentTypeForm(ModelForm):
    class Meta:
        model = ExternalContentType
        fields = ['name']


    def save(self, *args, **kw):
        self.instance.app_label = CONTENT_TYPE_EXTERNAL_APP_LABEL
        return super(ContentTypeForm, self).save(*args, **kw)


class PermissionForm(ModelForm):
    class Meta:
        model = ExternalPermission
        fields = ['name', 'content_type']


    def save(self, *args, **kw):
        self.instance.codename = '%s__%s' % (PERMISSION_EXTERNAL_CODE_NAME, uuid.uuid1())
        return super(PermissionForm, self).save(*args, **kw)