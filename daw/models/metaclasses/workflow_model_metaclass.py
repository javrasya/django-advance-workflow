from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from django.db.models.signals import pre_save, post_save

from daw.service.approvementservice import ApprovementService


__author__ = 'ahmetdal'


class WorkflowModelMetaclass(ModelBase):
    def __new__(cls, name, bases, attrs):
        result = super(WorkflowModelMetaclass, cls).__new__(cls, name, bases, attrs)

        pre_save.connect(_pre_save, result, False)
        post_save.connect(_post_save, result, False)

        return result


def _pre_save(*args, **kwargs):  # signal, sender, instance):
    """
    Desc: Set initial state of the object.
    :param kwargs:
    :return:
    """
    from daw.service.stateservice import StateService
    from daw.utils.fields import StateField

    instance = kwargs['instance']
    model = instance.__class__
    fields = []
    for f in model._meta.fields:
        if isinstance(f, StateField):
            fields.append(f)
    if model.objects.filter(pk=instance.pk).count() == 0:
        initial_state = StateService.get_init_state(ContentType.objects.get_for_model(instance))
        for f in fields:
            f.set_state(instance, initial_state)


def _post_save(*args, **kwargs):  # signal, sender, instance):
    """
    Desc:  Generate TransitionApprovements according to TransitionApproverDefinition of the content type at the beginning.
    :param kwargs:
    :return:
    """
    from daw.utils.fields import StateField
    from daw.models import TransitionApprovement

    instance = kwargs['instance']
    model = instance.__class__
    fields = []
    for f in model._meta.fields:
        if isinstance(f, StateField):
            fields.append(f)
    transition_approvements = TransitionApprovement.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
    if transition_approvements.count() == 0:
        for f in fields:
            ApprovementService._init_approvements(instance, f.name)