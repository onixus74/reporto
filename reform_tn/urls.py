from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import reform_tn


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reform_tn.views.home', name='home'),
    # url(r'^reform_tn/', include('reform_tn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^test$', 'base.views.test', name='test'),

    url(r'^$', 'base.views.home', name='home'),

    url(r'^reports/', include('reports.urls')),
    url(r'^reports-dashboard/', include('reports_dashboard.urls')),
    url(r'^report-submission/', include('report_submission.urls')),
    url(r'^categories/', include('categories.urls')),

)
