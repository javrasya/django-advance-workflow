from django import template
from django.contrib.contenttypes.models import ContentType

from daw.service.objectservice import ObjectService


register = template.Library()

__author__ = 'ahmetdal'

DAW_ON_APPROVAL_OBJECTS = 'on_approval_objects.html'


@register.inclusion_tag(DAW_ON_APPROVAL_OBJECTS, takes_context=True)
def daw_on_approval_objects(context, cls, state_field):
    content_type = ContentType.objects.get_for_model(cls)

    objects = ObjectService.get_objects_waiting_for_approval(content_type, state_field)

    ctx = context

    list_displays = context['list_displays']
    objs = []
    for object in objects:
        obj = []
        for list_display in list_displays:
            obj.append(getattr(object, list_display))
        objs.append(obj)

    ctx['objects'] = objs
    return ctx