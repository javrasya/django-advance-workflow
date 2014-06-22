from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.contrib.contenttypes.models import ContentType
from daw.service.approvement_service import ApprovementService

from daw.service.object_service import ObjectService


register = template.Library()

__author__ = 'ahmetdal'

DAW_PROCESS_BUTTON_MODALS_TEMPLATE = 'process_button_modals.html'


@register.inclusion_tag(DAW_PROCESS_BUTTON_MODALS_TEMPLATE, takes_context=True)
def daw_process_button_modals(context):
    return context