from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'report_submission.views.index', name='report_submission'),

)

