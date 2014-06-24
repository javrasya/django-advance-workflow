from daw.models import TransitionApprovement

__author__ = 'ahmetdal'


# noinspection PyClassHasNoInit
class ApproveDefinitionService:
    @staticmethod
    def apply_new_approve_definition(new_approve_definition):
        if new_approve_definition.transitionapprovement_set.count() == 0:
            content_type = new_approve_definition.transition.content_type
            model = content_type.model_class()
            for obj_pk in model.objects.values_list('pk', flat=True):
                TransitionApprovement.objects.create(approve_definition=new_approve_definition, content_type=content_type, object_pk=obj_pk)
