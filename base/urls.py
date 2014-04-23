from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
#from django.views.generic import TemplateView

#from base.utils.urls import administrator_required
from base.views import *
#from violations.views import ReportsDashboard

from users.views import user_profile_view

urlpatterns = patterns('',
                       url(r'^test/$', test_view, name='test'),

                       #url(r'^$', 'base.views.home', name='home'),
                       url(r'^$', home_view, name='home'),

                       # url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

                       url(r'', include('social_auth.urls')),

                       url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'login-minimal.html'}, name='login'),
                       # url(r'^signin/$',login_minimal_view,name='login'),
                       url(r'^signout/$', 'django.contrib.auth.views.logout', name='logout'),
                       #url(r'^signout/$', logout_view, name='logout'),
                       url(r'^signup/$', signup_view, name='signup'),
                       #url(r'^signup/1$', RegistrationView.as_view(), name='signup1'),

                       #(r'^accounts/', include('registration.backends.default.urls')),

                       #url(r'^activate/complete/$', ActivationView.as_view(), name='registration_activation_complete'),
                       #url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),


                       url(r'^user/password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
                       url(r'^user/password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
                       url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
                       url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
                       url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
                       url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
                       url(r'^user/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

                       #url(r'', include('django.contrib.auth.urls')),

                       # url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
                       # {'post_reset_redirect': '/user/password/reset/done/'}, name="password_reset"),
                       # url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
                       # url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
                       # {'post_reset_redirect': '/user/password/done/'}),
                       # url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

                       url(r'^user/profile(\.(?P<extension>(json)))?$', login_required(user_profile_view), name='users_profile'),

                       url(r'^users/', include('users.urls', namespace="users")),

                       url(r'^violations/', include('violations.urls', namespace='violations')),
                       url(r'^appreciations/', include('appreciations.urls', namespace='appreciations')),

                       #url(r'^public/statistics(\.(?P<extension>(json)))$', statistics_view, name='public_statistics'),
                       url(r'^public/statistics\.json$', statistics_view, name='public_statistics'),

                       url(r"^search/", include("watson.urls", namespace="search"), name='search'),
                       url(r'^report_builder/', include('report_builder.urls'))

                       )
