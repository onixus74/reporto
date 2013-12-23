from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from base.utils.urls import administrator_required

from base.views import *
from incidents.views import ReportsDashboard


urlpatterns = patterns('',
                       url(r'^test/$', test, name='test'),

                      (r'^i18n/', include('django.conf.urls.i18n')),

                       #url(r'^$', 'base.views.home', name='home'),
                       #url(r'^$',           login_required(ReportsDashboard.as_view(), login_url="login"),       name='home'),
                       url(r'^$',           login_required(home, login_url="login"),       name='home'),

                       # url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

                       url(r'^login/$',    login_view,    name='login'),
                       url(r'^logout/$',   logout_view,   name='logout'),
                       url(r'^register/$', register_view, name='register'),
                       url(r'',           include('django.contrib.auth.urls')),
                       url(r'',           include('social_auth.urls')),

                       url(r'^users/',      include('users.urls', namespace="users")),

                       url(r'^incidents/',    include('incidents.urls',    namespace='incidents')),
                       url(r'^thanks/',    include('thanks.urls',    namespace='thanks')),

                       url(r'^report_builder/', include('report_builder.urls'))

                       )
