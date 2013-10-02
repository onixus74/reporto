from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from base.utils.urls import administrator_required

from reports.views import *


urlpatterns = patterns('',

	url(r'^$', 'reports.views.index', name='reports'),

	url(r'^dashboard(\.(?P<extension>(json)))?$',           login_required(ReportsDashboard.as_view()),       name='dashboard'),
	#url(r'^submit$',             login_required(ReportSubmitView.as_view()),       name='submit'),
	url(r'^submit$',              login_required(report_submit),                    name='submit'),
	url(r'^submit/similar$',      login_required(similar_reports),                  name='similar_reports'),
	#url(r'^submit/ajax$',        login_required(submit_ajax),                      name='submit-ajax'),
	#url(r'^submit/public$',      ReportSubmitPublicView.as_view(), name='submit-public'),
	#url(r'^submit/upload$',      login_required(submit_upload),                     name='submit-upload'),
	url(r'^(?P<pk>\d+)/view(\.(?P<extension>(json)))?$',    login_required(ReportView.as_view()),             name='view'),
	url(r'^(?P<pk>\d+)/verify$',  login_required(report_verify),                    name='verify'),
	url(r'^(?P<pk>\d+)/close$',   login_required(report_close),                     name='close'),
	url(r'^(?P<pk>\d+)/comment$', login_required(report_comment),                   name='comment'),

	url(r'^(?P<pk>\d+)/comment$', login_required(report_comment),                   name='comment'),

	# url(r'^list$', ReportListView.as_view(), name='list'),
	# url(r'^crud(\.(?P<extension>(json)))?$',             ReportListHybridView.as_view(),   name='crud-list'),
	# url(r'^crud/new$',                                   ReportCreateView.as_view(),       name='crud-create'),
	# url(r'^crud/(?P<pk>\d+)(\.(?P<extension>(json)))?$', ReportDetailHybridView.as_view(), name='crud-view'),
	# url(r'^crud/(?P<pk>\d+)/edit$',                      ReportUpdateView.as_view(),       name='crud-edit'),
	# url(r'^crud/(?P<pk>\d+)/delete$',                    ReportDeleteView.as_view(),       name='crud-delete'),

)

