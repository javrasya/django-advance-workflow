from django import template
from django.contrib.contenttypes.models import ContentType

from daw.service.approvementservice import ApprovementService


register = template.Library()

__author__ = 'ahmetdal'

DAW_PROCESS_BUTTONS_TEMPLATE = 'process_buttons.html'


@register.inclusion_tag(DAW_PROCESS_BUTTONS_TEMPLATE, takes_context=True)
def daw_process_buttons(context, obj_pk, cls, state_field, approve_button_text=None, reject_button_text=None):
    cls = ContentType.objects.get_for_model(cls).model_class()
    obj = cls.objects.get(pk=obj_pk)
    waiting_approvements = ApprovementService.get_approvements_object_waiting_for_approval(obj, [getattr(obj, state_field)])

    ctx = context
    ctx['approvements'] = waiting_approvements
    ctx['obj_pk'] = obj_pk
    ctx['approve_button_text'] = approve_button_text
    ctx['reject_button_text'] = reject_button_text
    return ctx