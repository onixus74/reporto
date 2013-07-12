from django.conf.urls import patterns, url

from reports.views import ReportListView, ReportDetailView, ReportCreateView, ReportUpdateView, ReportDeleteView

urlpatterns = patterns('',

	url(r'^$', 'reports.views.index', name='reports'),
	url(r'^dashboard$', 'reports.views.dashboard', name='dashboard'),
	url(r'^submission$', 'reports.views.submission', name='submission'),
	url(r'^(?P<pk>\d+)$',  ReportDetailView.as_view(), name='report'),

	url(r'list$', ReportListView.as_view(), name='list'),
	url(r'new$', ReportCreateView.as_view(), name='create'),
	url(r'(?P<pk>\d+)/view$',  ReportDetailView.as_view(), name='view'),
	url(r'(?P<pk>\d+)/edit$',  ReportUpdateView.as_view(), name='edit'),
	url(r'(?P<pk>\d+)/delete$',  ReportDeleteView.as_view(), name='delete')

)

