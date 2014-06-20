from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.contrib.contenttypes.models import ContentType
from daw.service.approvement_service import ApprovementService

from daw.service.object_service import ObjectService


register = template.Library()

__author__ = 'ahmetdal'

DAW_PROCESS_BUTTON_TEMPLATE = 'process_buttons.html'


@register.inclusion_tag(DAW_PROCESS_BUTTON_TEMPLATE, takes_context=True)
def daw_process_buttons(context, obj_pk, cls, state_field):
    cls = ContentType.objects.get_for_model(cls).model_class()
    obj = cls.objects.get(pk=obj_pk)
    approvements = ApprovementService.get_approvements_object_waiting_for_approval(obj, [getattr(obj, state_field)])

    ctx = context
    ctx['approvements'] = approvements
    ctx['obj_pk'] = obj_pk
    return ctx