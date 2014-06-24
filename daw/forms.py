from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm


class ContentTypeForm(ModelForm):
    class Meta:
        model = ContentType
        fields = ['name']


    def save(self, *args, **kw):
        self.instance.app_label = settings.CONTENT_TYPE_EXTERNAL_APP_LABEL
        return super(ContentTypeForm, self).save(*args, **kw)