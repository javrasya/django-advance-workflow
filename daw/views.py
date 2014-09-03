# Create your views here.
import json
import urllib
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from daw.models import State

from daw.service.approvementservice import ApprovementService
from daw.service.transitionservice import TransitionService


def init_object_approvements_view(request, content_type_id, obj_pk, state_field):
    try:
        ApprovementService.init_approvements(content_type_id, obj_pk, state_field)
        return HttpResponse(json.dumps({}), content_type='application/json')

    except Exception, e:
        return HttpResponseBadRequest(json.dumps({'error_message': e.message}), content_type='application/json')


def approve_transition_view(request, content_type_id, obj_pk, state_field, next_state_id=None):
    try:
        TransitionService.approve_transition(content_type_id, obj_pk, state_field, next_state_id)
        return HttpResponse(json.dumps({}), content_type='application/json')
    except Exception, e:
        return HttpResponseBadRequest(json.dumps({'error_message': e.message}), content_type='application/json')


def reject_transition_view(request, content_type_id, obj_pk, state_field, next_state_id=None):
    try:
        TransitionService.reject_transition(content_type_id, obj_pk, state_field, next_state_id)
        return HttpResponse(json.dumps({}), content_type='application/json')
    except Exception, e:
        return HttpResponseBadRequest(json.dumps({'error_message': e.message}), content_type='application/json')


def get_current_state(request, content_type_id, obj_pk, state_field):
    content_type = ContentType.objects.get(pk=content_type_id)
    model = content_type.model_class()
    obj = model.objects.get(pk=obj_pk)
    state = getattr(obj, state_field)
    return HttpResponse(json.dumps({'id': state.pk, 'label': state.label}), content_type='application/json')


def get_state_by_label(request, label):
    state = State.objects.get(label=label)
    return HttpResponse(json.dumps({'id': state.pk, 'label': state.label}), content_type='application/json')


def _get_decoded_callback_url(url):
    return urllib.unquote(url).decode('iso-8859-2')