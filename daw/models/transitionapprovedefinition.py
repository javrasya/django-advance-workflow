from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _
from daw.models import Transition


__author__ = 'ahmetdal'


class TransitionApproveDefinition(models.Model):
    class Meta:
        verbose_name = _("Transition Approve Definition")
        verbose_name_plural = _("Transition Approve Definitions")
        db_table = "daw_transition_approve_definition"
        app_label = "daw"
        unique_together = [('transition', 'permission'), ('transition', 'permission', 'order')]

    transition = models.ForeignKey(Transition, verbose_name=_('Transition'))
    permission = models.ForeignKey(Permission, verbose_name=_('Permission'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    def save(self, *args, **kwargs):
        max_order = TransitionApproveDefinition.objects.latest('order').order
        self.order = max_order + 1
        super(TransitionApproveDefinition, self).save(*args, **kwargs)










