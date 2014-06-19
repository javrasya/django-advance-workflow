__author__ = 'ahmetdal'

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, pre_save

from daw.models import TransitionApprovement
from daw.service.approvement_service import ApprovementService


class StateField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super(StateField, self).__init__(*args, **kwargs)


    def contribute_to_class(self, cls, name, virtual_only=False):
        self.base_cls = cls

        super(StateField, self).contribute_to_class(cls, name, virtual_only=virtual_only)

        pre_save.connect(self._pre_save, cls, True)
        post_save.connect(self._post_save, cls, True)


    def _pre_save(self, **kwargs):  # signal, sender, instance):
        """
        Desc: Set initial state of the object.
        :param kwargs:
        :return:
        """
        from daw.service.state_service import StateService

        instance = kwargs['instance']
        if not instance.pk:
            initial_state = StateService.get_init_state(ContentType.objects.get_for_model(instance))
            self.set_state(instance, initial_state)

    def _post_save(self, **kwargs):  # signal, sender, instance):
        """
        Desc:  Generate TransitionApprovements according to TransitionApproverDefinition of the content type at the beginning.
        :param kwargs:
        :return:
        """
        instance = kwargs['instance']
        transition_approvements = TransitionApprovement.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
        if transition_approvements.count() == 0:
            ApprovementService.init_approvements(instance)


    def get_state(self, instance):
        return instance.__dict__[self.attname]

    def set_state(self, instance, state):
        instance.__dict__[self.attname] = self.to_python(state)

