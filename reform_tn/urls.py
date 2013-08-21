from django.conf.urls import patterns, include, url

from filebrowser.sites import site
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/grappelli/', include('grappelli.urls')),
    url(r'', include('base.urls')),

)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
