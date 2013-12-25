from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, \
    permission_required
from django.views.generic import TemplateView

from base.utils.urls import administrator_required
from base.views import *
from violations.views import ReportsDashboard


urlpatterns = patterns('',
                       url(r'^test/$', test_view, name='test'),

                      (r'^i18n/', include('django.conf.urls.i18n')),

                       #url(r'^$', 'base.views.home', name='home'),
                       url(r'^$', home_view, name='home'),

                       # url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

                       url(r'^login/$',    login_view,    name='login'),
                       url(r'^logout/$',   logout_view,   name='logout'),
                       url(r'^register/$', register_view, name='register'),
                       url(r'',           include('django.contrib.auth.urls')),
                       url(r'',           include('social_auth.urls')),

                       url(r'^users/',      include('users.urls', namespace="users")),

                       url(r'^violations/',    include('violations.urls',    namespace='violations')),
                       url(r'^thanks/',    include('thanks.urls',    namespace='thanks')),

                       url(r"^search/", include("watson.urls", namespace="search"), name='search'),
                       url(r'^report_builder/', include('report_builder.urls'))

                       )
