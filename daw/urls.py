from django.conf.urls import patterns, url

urlpatterns = patterns('daw.views',
                       url(
                           r'^init_object_approvements/(?P<content_type_id>[$a-zA-Z0-9]+)/(?P<obj_pk>[$a-zA-Z0-9]+)/(?P<state_field>[$a-zA-Z0-9_]+)/(?P<callback_url>[$a-zA-Z0-9%:_.]+)/$',
                           'init_object_approvements_view'),
                       url(
                           r'^approve_transition/(?P<content_type_id>[$a-zA-Z0-9]+)/(?P<obj_pk>[$a-zA-Z0-9]+)/(?P<state_field>[$a-zA-Z0-9_]+)/(?:(?P<next_state_id>[$a-zA-Z0-9]+)/)?$',
                           'approve_transition_view'),
                       url(
                           r'^reject_transition/(?P<content_type_id>[$a-zA-Z0-9]+)/(?P<obj_pk>[$a-zA-Z0-9]+)/(?P<state_field>[$a-zA-Z0-9_]+)/(?:(?P<next_state_id>[$a-zA-Z0-9]+)/)?$',
                           'reject_transition_view'),

                       url(
                           r'^get_current_state/(?P<content_type_id>[$a-zA-Z0-9]+)/(?P<obj_pk>[$a-zA-Z0-9]+)/(?P<state_field>[$a-zA-Z0-9_]+)/?$', 'get_current_state'),
                       url(
                           r'^get_state_by_label/(?P<label>[$a-zA-Z0-9]+)/?$', 'get_state_by_label'),
                       url(
                           r'^skip_transition/(?P<content_type_id>[$a-zA-Z0-9]+)/(?P<object_id>[$a-zA-Z0-9]+)/(?P<state_field>[$a-zA-Z0-9_]+)/(?P<destination_state_id>[$a-zA-Z0-9]+)/?$',
                           'skip_transition'),

)
