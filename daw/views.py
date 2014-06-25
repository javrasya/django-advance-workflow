# Create your views here.
import urllib

from django.http import HttpResponseRedirect

from daw.service.approvementservice import ApprovementService
from daw.service.transitionservice import TransitionService


def init_object_approvements_view(request, content_type_id, obj_pk, state_field, callback_url):
    callback_url = _get_decoded_callback_url(callback_url)
    try:
        ApprovementService.init_approvements(content_type_id, obj_pk)
        callback_url += '?result=success'
    except Exception, e:
        callback_url += '?result=failed&error_message=%s' % e.message
    return HttpResponseRedirect(callback_url)


def approve_transition_view(request, content_type_id, obj_pk, state_field, callback_url, next_state_id=None):
    callback_url = _get_decoded_callback_url(callback_url)
    try:
        TransitionService.approve_transition(content_type_id, obj_pk, state_field, next_state_id)
        callback_url += '?result=success'
    except Exception, e:
        callback_url += '?result=failed&error_message=%s' % e.message
    return HttpResponseRedirect(callback_url)


def reject_transition_view(request, content_type_id, obj_pk, state_field, callback_url, next_state_id=None):
    callback_url = _get_decoded_callback_url(callback_url)
    try:
        TransitionService.reject_transition(content_type_id, obj_pk, state_field, next_state_id)
        callback_url += '?result=success'
    except Exception, e:
        callback_url += '?result=failed&error_message=%s' % e.message
    return HttpResponseRedirect(callback_url)


def _get_decoded_callback_url(url):
    return urllib.unquote(url).decode('iso-8859-2')