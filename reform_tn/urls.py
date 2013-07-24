from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reform_tn.views.home', name='home'),
    # url(r'^reform_tn/', include('reform_tn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin'),

    url(r'^test/$', 'base.views.test', name='test'),

    #url(r'^$', 'base.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^categories/', include('categories.urls', namespace="categories")),
    url(r'^features/', include('features.urls', namespace="features")),
    url(r'^victims/', include('victims.urls', namespace="victims")),


    #url(r'^fu1$', 'base.views.fu1', name='fu1'),
    #url(r'^fu2$', 'base.views.fu2', name='fu2'),

)
