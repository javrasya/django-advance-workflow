from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'django_advance_workflow.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
                       url(r'^daw/', include('daw.urls')),
                       url(r'^$', include('example_app.urls')),
                       url(r'^example_app/', include('example_app.urls')),

)
