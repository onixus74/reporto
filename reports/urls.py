from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'reports.views.index', name='reports'),
    url(r'^dashboard$', 'reports.views.dashboard', name='dashboard'),
    url(r'^submission$', 'reports.views.submission', name='submission'),

)

