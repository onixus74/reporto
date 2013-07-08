from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'reports_dashboard.views.index', name='reports_dashboard'),

)

