from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


urlpatterns = patterns('',
	url(r'^test/$', 'base.views.test', name='test'),

	url(r'^$', 'base.views.home', name='home'),
	# url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

	url(r'^login$',  'base.views.login_view', name='login'),
	url(r'^logout$', 'base.views.logout_view', name='logout'),
	#url(r'^users/', include('django.contrib.auth.urls')),

	url(r'^reports/',    include('reports.urls',    namespace='reports')),
	url(r'^categories/', include('categories.urls', namespace="categories")),
	url(r'^features/',   include('features.urls',   namespace="features")),
	url(r'^victims/',    include('victims.urls',    namespace="victims")),

	url(r'^users/',      include('base.users_urls', namespace="users")),

)
