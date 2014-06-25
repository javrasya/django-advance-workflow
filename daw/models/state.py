from django.db import models
from django.utils.translation import ugettext_lazy as _

from daw.models.base_model import BaseModel


__author__ = 'ahmetdal'


class State(BaseModel):
    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
        db_table = "daw_state"
        app_label = "daw"

    label = models.CharField(max_length=50)
    description = models.TextField(_("Description"), max_length=200, null=True, blank=True)


    def __unicode__(self):
        return '%s%s' % (self.label, self.description and '(%s)' % self.description)






