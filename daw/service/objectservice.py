from daw.service.approvementservice import ApprovementService


__author__ = 'ahmetdal'


class ObjectService:
    def __init__(self):
        pass

    @staticmethod
    def get_objects_waiting_for_approval(content_type, field):
        model = content_type.model_class()
        object_pks = []
        for obj in model.objects.all():
            current_state = getattr(obj, field)
            approvements = ApprovementService.get_approvements_object_waiting_for_approval(obj, [current_state])
            if approvements.count():
                object_pks.append(obj.pk)
        return model.objects.filter(pk__in=object_pks)


