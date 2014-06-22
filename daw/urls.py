from django.conf.urls import patterns, url

urlpatterns = patterns('daw.views',
                       url(
                           r'^approve_transition/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<obj_pk>[a-zA-Z0-9]+)/(?P<state_field>[a-zA-Z0-9]+)/(?P<callback_url>[a-zA-Z0-9%:_.]+)/(?:(?P<next_state_id>[a-zA-Z0-9]+)/)?$',
                           'approve_transition_view'),


)
