# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from daw.utils.signals import post_transition, pre_transition
from daw.utils.transition_event import transition_event_registry, BEFORE, AFTER


def on_pre_transition(sender, instance, name, source, target, **kwargs):
    transition_event = transition_event_registry.get('%s%s%s%s' % (ContentType.objects.get_for_model(instance), source, target, BEFORE))
    transition_event.execute()


def on_post_transition(sender, instance, name, source, target, **kwargs):
    transition_event = transition_event_registry.get('%s%s%s%s' % (ContentType.objects.get_for_model(instance), source, target, AFTER))
    transition_event.execute()


pre_transition.connect(on_pre_transition)
post_transition.connect(on_post_transition)
