from daw.models.managers.basemanager import BaseModelManager


__author__ = 'ahmetdal'


class TransitionApproveDefinitionManager(BaseModelManager):
    def create(self, **kwargs):
        from daw.service.approvedefinitionservice import ApproveDefinitionService

        transition_approve_definition = super(TransitionApproveDefinitionManager, self).create(**kwargs)
        ApproveDefinitionService.apply_new_approve_definition(transition_approve_definition)













