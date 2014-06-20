from django.conf.urls import patterns, url

urlpatterns = patterns('example_app.views',
                       url(r'^on_approval_objects$', 'on_approval_objects'),
                       url(r'^process_buttons$', 'process_buttons'),


)
