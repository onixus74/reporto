from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from reports.views import *
from reports.api import router

urlpatterns = patterns('',

	url(r'^$', 'reports.views.index', name='reports'),

	#url(r'^dashboard$', 'reports.views.dashboard', name='dashboard'),
	#url(r'^submission$', 'reports.views.submission', name='submission'),
	#url(r'^submission_json$', 'reports.views.submission_json', name='submission'),
	#url(r'^submission$', ReportSubmission.as_view(), name='submission'),

	url(r'^dashboard$',           login_required(ReportsDashboard.as_view()),       name='dashboard'),
	#url(r'^submit$',             login_required(ReportSubmitView.as_view()),       name='submit'),
	url(r'^submit$',              login_required(report_submit),       name='submit'),
	#url(r'^submit/ajax$',        login_required(submit_ajax),                      name='submit-ajax'),
	#url(r'^submit/public$',      ReportSubmitPublicView.as_view(), name='submit-public'),
	#url(r'^submit/upload$',      login_required(submit_upload),                    name='submit-upload'),
	url(r'^(?P<pk>\d+)/view$',    login_required(ReportView.as_view()),             name='view'),
	url(r'^(?P<pk>\d+)/verify$',  login_required(report_verify),                    name='verify'),
	url(r'^(?P<pk>\d+)/close$',   login_required(report_close),                     name='close'),
	url(r'^(?P<pk>\d+)/comment$', login_required(report_comment),                   name='comment'),

	#url(r'^list$', ReportListView.as_view(), name='list'),
	url(r'^manage(\.(?P<extension>(json)))?$',        ReportListHybridView.as_view(),   name='manage-list'),
	url(r'^manage/new$',                                   ReportCreateView.as_view(),       name='manage-create'),
	url(r'^manage/(?P<pk>\d+)(\.(?P<extension>(json)))?$', ReportDetailHybridView.as_view(), name='manage-view'),
	url(r'^manage/(?P<pk>\d+)/edit$',                      ReportUpdateView.as_view(),       name='manage-edit'),
	url(r'^manage/(?P<pk>\d+)/delete$',                    ReportDeleteView.as_view(),       name='manage-delete'),

	url(r'^api', include(router.urls)),

)

