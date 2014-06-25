from django.contrib.contenttypes.models import ContentType
from django.db.models import Min, Q

from daw.utils import middleware
from daw.models import State
from daw.models.transitionapprovedefinition import TransitionApproveDefinition
from daw.models.transitionapprovement import TransitionApprovement, PENDING


__author__ = 'ahmetdal'


class ApprovementService:
    def __init__(self):
        pass

    @staticmethod
    def init_approvements(content_type_id, obj_pk):
        content_type = ContentType.objects.get(pk=content_type_id)
        model = content_type.model_class()
        obj = model.objects.get(pk=obj_pk)
        ApprovementService._init_approvements(obj)


    @staticmethod
    def _init_approvements(obj):
        content_type = ContentType.objects.get_for_model(obj)
        for transition_approve_definition in TransitionApproveDefinition.objects.filter(transition__content_type=content_type):
            TransitionApprovement.objects.update_or_create(
                approve_definition=transition_approve_definition,
                object_pk=obj.pk,
                content_type=content_type,
                defaults={
                    'status': PENDING
                }
            )

    @staticmethod
    def get_approvements_object_waiting_for_approval(obj, source_states, include_user=True, destination_state=None):

        content_type = ContentType.objects.get_for_model(obj)
        approvements = TransitionApprovement.objects.filter(
            content_type=content_type,
            object_pk=obj.pk,
            approve_definition__transition__source_state__in=source_states,
            status=PENDING
        )
        min_order = approvements.aggregate(Min('approve_definition__order'))['approve_definition__order__min']
        approvements = approvements.filter(approve_definition__order=min_order)
        if include_user:
            user = middleware.get_user()
            approvements = approvements.filter(Q(transactioner=user) | Q(approve_definition__permission__in=user.user_permissions.all()))
        if destination_state:
            approvements = approvements.filter(approve_definition__transition__destination_state=destination_state)

        unskipped_approvements = approvements.filter(skip=False)

        if approvements.count() == 0:
            return approvements
        elif unskipped_approvements.count() != 0:
            return unskipped_approvements
        else:
            source_state_pks = approvements.values_list('approve_definition__transition__destination_state', flat=True)
            return ApprovementService.get_approvements_object_waiting_for_approval(obj, State.objects.filter(pk__in=source_state_pks), include_user=False)


















