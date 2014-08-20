from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
#from filebrowser.sites import site


admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^a/', include(admin.site.urls), name='admin'),
                       #url(r'^admin/filebrowser/', include(site.urls)),
                       #url(r'^admin/grappelli/', include('grappelli.urls')),

                      (r'^i18n/', include('django.conf.urls.i18n')),
                      (r'^i18n/js/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog', {
                       #'domain': 'djangojs',
                       #'packages': ('base',),
                       }, 'i18n_js'),
                      (r'^i18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog', {
                       'domain': 'django',
                       #'packages': ('base',),
                       }, 'i18n'),
                       )


urlpatterns += patterns('', url(r'', include('base.urls')))
# urlpatterns += i18n_patterns('', url(r'', include('base.urls')))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'})

if settings.DEBUG:
    urlpatterns += patterns('',
                           (r'^500/$', 'django.views.defaults.server_error'),
                           (r'^404/$', TemplateView.as_view(template_name='404.html')),
                            )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )
