from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from daw.utils import middleware
from daw.models import APPROVED, REJECTED
from daw.service.approvement_service import ApprovementService
from daw.service.state_service import StateService

__author__ = 'ahmetdal'


class TransitionService:
    def __init__(self):
        pass


    @staticmethod
    def approve_transition(content_type_id, obj_pk, field, state=None):
        content_type = ContentType.objects.get(pk=content_type_id)
        model = content_type.model_class()
        obj = model.objects.get(pk=obj_pk)
        TransitionService._approve_transition(obj, field, state)


    @staticmethod
    def _approve_transition(obj, field, state=None):
        approvement = TransitionService.process(obj, field, APPROVED, state)
        current_state = getattr(obj, field)
        required_approvements = ApprovementService.get_approvements_object_waiting_for_approval(obj, [current_state], include_user=False, destination_state=state)
        if required_approvements.count() == 0:
            setattr(obj, field, approvement.approve_definition.transition.destination_state)
            obj.save()


    @staticmethod
    def reject_transition(obj, field, state=None):
        TransitionService.process(obj, field, REJECTED, state)

    @staticmethod
    def process(obj, field, action, state=None):
        current_state = getattr(obj, field)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(obj, [current_state])
        c = approvements.count()
        if c == 0:
            raise Exception("There is no available state for destination for the user.")
        if c > 1:
            if state:
                approvements = approvements.filter(approve_definition__transition__destination_state=state)
                if approvements.count() == 0:
                    available_states = StateService.get_available_states(obj, field)
                    raise Exception("Invalid state is given(%s). Valid states is(are) %s" % (state.__unicode__(), ','.join([ast.__unicode__() for ast in available_states])))
            else:
                raise Exception("State must be given when there are multiple states for destination")
        approvement = approvements[0]
        approvement.status = action
        approvement.transactioner = middleware.get_user()
        approvement.transaction_date = datetime.now()
        approvement.save()
        return approvement