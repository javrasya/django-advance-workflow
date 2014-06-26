from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from daw.models import State, BaseModel


__author__ = 'ahmetdal'


class Transition(BaseModel):
    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")
        db_table = "daw_transition"
        app_label = "daw"

    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'))
    source_state = models.ForeignKey(State, verbose_name=_("Source State"), related_name='transitions_as_source')
    destination_state = models.ForeignKey(State, verbose_name=_("Next State"), related_name='transitions_as_destination')


    def __unicode__(self):
        return '%s -> %s (%s)' % (self.source_state, self.destination_state, self.content_type)



