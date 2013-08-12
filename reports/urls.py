from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, permission_required

from reports.views import *
from reports.api import router

urlpatterns = patterns('',

	url(r'^$', 'reports.views.index', name='reports'),

	#url(r'^dashboard$', 'reports.views.dashboard', name='dashboard'),
	#url(r'^submission$', 'reports.views.submission', name='submission'),
	#url(r'^submission_json$', 'reports.views.submission_json', name='submission'),
	#url(r'^submission$', ReportSubmission.as_view(), name='submission'),

	url(r'^dashboard$',          ReportsDashboard.as_view(),       name='dashboard'),
	url(r'^submit$',             ReportSubmitView.as_view(),       name='submit'),
	url(r'^submit/ajax$',        submit_ajax,                      name='submit-ajax'),
	url(r'^submit/public$',      ReportSubmitPublicView.as_view(), name='submit-public'),
	url(r'^submit/upload$',      submit_upload,                    name='submit-public'),
	url(r'^(?P<pk>\d+)/view$',   ReportView.as_view(),             name='view'),
	url(r'^(?P<pk>\d+)/verify$', ReportVerifyView.as_view(),       name='verify'),
	url(r'^(?P<pk>\d+)/close$',  ReportCloseView.as_view(),        name='close'),

	#url(r'^list$', ReportListView.as_view(), name='list'),
	url(r'^manage(\.(?P<extension>(json)))?$',        ReportListHybridView.as_view(),   name='manage-list'),
	url(r'^manage/new$',                                   ReportCreateView.as_view(),       name='manage-create'),
	url(r'^manage/(?P<pk>\d+)(\.(?P<extension>(json)))?$', ReportDetailHybridView.as_view(), name='manage-view'),
	url(r'^manage/(?P<pk>\d+)/edit$',                      ReportUpdateView.as_view(),       name='manage-edit'),
	url(r'^manage/(?P<pk>\d+)/delete$',                    ReportDeleteView.as_view(),       name='manage-delete'),

	url(r'^api', include(router.urls)),

)

