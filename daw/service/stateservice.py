from django.contrib.contenttypes.models import ContentType

from daw.utils import middleware
from daw.models import State, TransitionApprovement


__author__ = 'ahmetdal'


class StateService:
    def __init__(self):
        pass

    @staticmethod
    def get_available_states(obj, field, include_user=True):
        content_type = ContentType.objects.get_for_model(obj)
        current_state = getattr(obj, field)
        approvements = TransitionApprovement.objects.filter(
            content_type=content_type,
            object_pk=obj.pk,
            approve_definition__transition__source_state=current_state,
        )
        if include_user:
            user = middleware.get_user()
            approvements = approvements.filter(
                approve_definition__permission__in=user.user_permissions.all()
            )
        destination_states = approvements.values_list('approve_definition__transition__destination_state', flat=True)
        return State.objects.filter(pk__in=destination_states)


    @staticmethod
    def get_init_state(content_type):
        initial_state_candidates = State.objects.filter(
            transitions_as_source__isnull=False,
            transitions_as_source__content_type=content_type,
            transitions_as_destination__isnull=True,
        ).distinct()
        c = initial_state_candidates.count()
        if c == 0:
            raise Exception('There is no available initial state for the content type %s. Insert a state which is not a destination in a transition.' % content_type)
        elif c > 1:
            raise Exception('There are multiple initial state for the content type %s. Have only one initial state' % content_type)

        return initial_state_candidates[0]















