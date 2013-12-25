from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, \
    permission_required

from base.utils.urls import administrator_required

from .views import *


urlpatterns = patterns('',

                       #url(r'^$', 'violations.views.index', name='reports'),

                       url(r'^(\.(?P<extension>(json)))?$',           login_required(ReportsDashboard.as_view()),       name='dashboard'),
                       #url(r'^submit$',             login_required(ReportSubmitView.as_view()),       name='submit'),
                       url(r'^submit$',              login_required(report_submit),                    name='submit'),
                       url(r'^submit/similar$',      login_required(similar_reports),                  name='similar_reports'),
                       #url(r'^submit/ajax$',        login_required(submit_ajax),                      name='submit-ajax'),
                       #url(r'^submit/public$',      ReportSubmitPublicView.as_view(), name='submit-public'),
                       #url(r'^submit/upload$',      login_required(submit_upload),                     name='submit-upload'),
                       url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$',    login_required(ReportView.as_view()),             name='view'),
                       url(r'^(?P<pk>\d+)/partial$',    login_required(ReportPartialView.as_view()),             name='view_pupdate'),
                       #url(r'^(?P<pk>\d+)$',    login_required(ReportView.as_view()),             name='view'),
                       url(r'^(?P<pk>\d+)/update$',  login_required(report_update),                    name='update_partial'),
                       url(r'^(?P<pk>\d+)/verify$',  login_required(report_verify),                    name='verify'),
                       url(r'^(?P<pk>\d+)/close$',   login_required(report_close),                     name='close'),
                       url(r'^(?P<pk>\d+)/comment$', login_required(report_comment),                   name='comment'),


                       url(r'^public/statistics$', statistics,         name='public_statistics'),
                       #url(r'^public/statistics/by-date$', statistics_reports_by_date,         name='public_statistics_reports_by_date'),

                       url(r'^crud/(\.(?P<extension>(json)))?$',            administrator_required(ReportListHybridView.as_view()),   name='crud-list'),
                       url(r'^crud/new$',                                   administrator_required(ReportCreateView.as_view()),       name='crud-create'),
                       url(r'^crud/(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(ReportDetailHybridView.as_view()), name='crud-view'),
                       url(r'^crud/(?P<pk>\d+)/edit$',                      administrator_required(ReportUpdateView.as_view()),       name='crud-edit'),
                       url(r'^crud/(?P<pk>\d+)/delete$',                    administrator_required(ReportDeleteView.as_view()),       name='crud-delete'),

                       url(r'^categories/', include('violations_categories.urls', namespace="categories")),
                       url(r'^features/',   include('violations_features.urls', namespace="features")),
                       url(r'^victims/',    include('violations_victims.urls', namespace="victims")),

                       )
