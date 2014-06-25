from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _

from daw.models import Transition, BaseModel
from daw.models.managers.transitionapprovedefinitionmanager import TransitionApproveDefinitionManager


__author__ = 'ahmetdal'


class TransitionApproveDefinition(BaseModel):
    class Meta:
        verbose_name = _("Transition Approve Definition")
        verbose_name_plural = _("Transition Approve Definitions")
        db_table = "daw_transition_approve_definition"
        app_label = "daw"
        unique_together = [('transition', 'permission'), ('transition', 'permission', 'order')]

    transition = models.ForeignKey(Transition, verbose_name=_('Transition'))
    permission = models.ForeignKey(Permission, verbose_name=_('Permission'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    objects = TransitionApproveDefinitionManager()

    def save(self, *args, **kwargs):
        from daw.service.approvedefinitionservice import ApproveDefinitionService

        super(TransitionApproveDefinition, self).save(*args, **kwargs)
        ApproveDefinitionService.apply_new_approve_definition(self)












