from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from daw.models import TransitionApproveDefinition, BaseModel


__author__ = 'ahmetdal'

PENDING = '0'
APPROVED = '1'
REJECTED = '2'

APPROVMENT_STATUSES = [
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (REJECTED, _('Rejected')),
]


class TransitionApprovement(BaseModel):
    class Meta:
        verbose_name = _("Transition Approvement")
        verbose_name_plural = _("Transition Approvements")
        db_table = "daw_transition_approvement"
        app_label = "daw"

    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'), )
    object_pk = models.PositiveIntegerField(verbose_name=_('Related Object'))
    object = generic.GenericForeignKey('content_type', 'object_pk')

    approve_definition = models.ForeignKey(TransitionApproveDefinition, verbose_name=_('Approve Definition'))
    transactioner = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), verbose_name=_('Approver'), null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(_('Status'), max_length=20, choices=APPROVMENT_STATUSES, default=PENDING)

    skip = models.BooleanField(_('Skip'), default=False)












