from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
#from filebrowser.sites import site


admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls), name='admin'),
                       #url(r'^admin/filebrowser/', include(site.urls)),
                       #url(r'^admin/grappelli/', include('grappelli.urls')),
                       url(r'', include('base.urls')),

                       )


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'})
