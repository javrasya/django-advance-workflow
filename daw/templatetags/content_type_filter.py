from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()

__author__ = 'ahmetdal'


@register.filter(name='content_type')
def content_type(cls):
    return ContentType.objects.get_for_model(cls)
