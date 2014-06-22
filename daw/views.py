# Create your views here.
import urllib

from django.http import HttpResponseRedirect
from daw.service.transition_service import TransitionService


def approve_transition_view(request, content_type_id, obj_pk, state_field, callback_url, next_state_id=None):
    callback_url = urllib.unquote(callback_url).decode('iso-8859-2')
    try:
        TransitionService.approve_transition(content_type_id, obj_pk, state_field, next_state_id)
        callback_url += '?result=success'
    except Exception, e:
        callback_url += '?result=failed&error_message=%s' % e.message
    return HttpResponseRedirect(callback_url)
