from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from daw import CONTENT_TYPE_EXTERNAL_APP_LABEL


class ContentTypeForm(ModelForm):
    class Meta:
        model = ContentType
        fields = ['name']


    def save(self, *args, **kw):
        self.instance.app_label = CONTENT_TYPE_EXTERNAL_APP_LABEL
        return super(ContentTypeForm, self).save(*args, **kw)