from django.conf.urls import patterns, url

urlpatterns = patterns('daw.views',
                       url(
                           r'^init_object_approvements/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<obj_pk>[a-zA-Z0-9]+)/(?P<state_field>[a-zA-Z0-9]+)/(?P<callback_url>[a-zA-Z0-9%:_.]+)/$',
                           'init_object_approvements_view'),
                       url(
                           r'^approve_transition/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<obj_pk>[a-zA-Z0-9]+)/(?P<state_field>[a-zA-Z0-9]+)/(?P<callback_url>[a-zA-Z0-9%:_.]+)/(?:(?P<next_state_id>[a-zA-Z0-9]+)/)?$',
                           'approve_transition_view'),
                       url(
                           r'^reject_transition/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<obj_pk>[a-zA-Z0-9]+)/(?P<state_field>[a-zA-Z0-9]+)/(?P<callback_url>[a-zA-Z0-9%:_.]+)/(?:(?P<next_state_id>[a-zA-Z0-9]+)/)?$',
                           'reject_transition_view'),
)
