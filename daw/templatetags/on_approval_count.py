from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext

from daw.service.objectservice import ObjectService


register = template.Library()

__author__ = 'ahmetdal'

DAW_ON_APPROVAL_COUNT = 'on_approval_count.html'


@register.inclusion_tag(DAW_ON_APPROVAL_COUNT, takes_context=True)
def daw_on_approval_count(context, cls, state_field, button_href, button_text=ugettext('On Approvals')):
    content_type = ContentType.objects.get_for_model(cls)

    objects = ObjectService.get_objects_waiting_for_approval(content_type, state_field)

    ctx = context

    ctx['on_approval_count_button_href'] = button_href
    ctx['on_approval_count_button_text'] = button_text
    ctx['on_approval_count'] = objects.count()
    return ctx