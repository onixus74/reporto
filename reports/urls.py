from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from reports.views import *

urlpatterns = patterns('',

	url(r'^$', 'reports.views.index', name='reports'),
	#url(r'^dashboard$', 'reports.views.dashboard', name='dashboard'),
	url(r'^dashboard$', ReportsDashboard.as_view(), name='dashboard'),
	#url(r'^submission$', 'reports.views.submission', name='submission'),
	url(r'^submission_json$', 'reports.views.submission_json', name='submission'),
	url(r'^submission$', ReportSubmission.as_view(), name='submission'),



	#url(r'list$', ReportListView.as_view(), name='list'),
	url(r'list(\.(?P<extension>(json)))?$', ReportListMultiView.as_view(), name='list'),
	url(r'new$', ReportCreateView.as_view(), name='create'),
	url(r'(?P<pk>\d+)(\.(?P<extension>(json)))?$', ReportDetailMultiView.as_view(), name='view'),
	url(r'(?P<pk>\d+)/edit$', ReportUpdateView.as_view(), name='edit'),
	url(r'(?P<pk>\d+)/delete$', ReportDeleteView.as_view(), name='delete'),

	url(r'(?P<pk>\d+)/verify$', ReportDetailView.as_view(), name='verify'),
	url(r'(?P<pk>\d+)/close$', ReportDetailView.as_view(), name='close'),

)

