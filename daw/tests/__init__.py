from django.db.models.signals import pre_save

from daw.models.transition import Transition


__author__ = 'ahmetdal'


def _pre_save(*args, **kwargs):
    instance = kwargs['instance']
    instance.content_type = ContentType.objects.get_for_model(TestModel)


pre_save.connect(_pre_save, Transition)

from base_test import *
from state_service_test import *
from approvement_service_test import *
from transition_service_test import *
from object_service_test import *