from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from daw.models.managers.basemanager import BaseModelManager

from daw.utils.middleware import get_user


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Created At'), null=True, blank=True)
    last_updated_at = models.DateTimeField(_('Last Updated At'), null=True, blank=True)
    created_by = models.CharField(_('Created By'), max_length=200, null=True, blank=True)
    last_updated_by = models.CharField(_('Last Updated By'), max_length=200, null=True, blank=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_user()
        self.last_updated_at = datetime.now()
        self.last_updated_by = user and user.username or None
        if not self.id:
            self.created_at = datetime.now()
            self.created_by = user and user.username or None

        super(BaseModel, self).save(*args, **kwargs)
