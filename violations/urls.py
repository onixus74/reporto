from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from base.utils.urls import login_required_with_message, administrator_required

from .views import *


urlpatterns = patterns('',

                       #url(r'^$', 'violations.views.index', name='reports'),

                       url(r'^(\.(?P<extension>(json)))?$',       administrator_required(ReportsDashboard.as_view()),       name='dashboard'),
                       url(r'^search(\.(?P<extension>(json)))?$', ReportSearchView.as_view(),       name='search'),
                       #url(r'^submit$',             login_required_with_message(ReportSubmitView.as_view()),       name='submit'),
                       url(r'^submit$',              login_required_with_message(report_submit),                    name='submit'),
                       url(r'^submit/similar$',      login_required(similar_reports),                  name='similar_reports'),
                       #url(r'^submit/ajax$',        login_required(submit_ajax),                      name='submit-ajax'),
                       #url(r'^submit/public$',      ReportSubmitPublicView.as_view(), name='submit-public'),
                       #url(r'^submit/upload$',      login_required(submit_upload),                     name='submit-upload'),
                       url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', ReportView.as_view(),           name='view'),
                       url(r'^(?P<pk>\d+)/partial$', ReportPartialView.as_view(),                      name='view_partial'),
                       #url(r'^(?P<pk>\d+)$',         login_required(ReportView.as_view()),             name='view'),
                       url(r'^(?P<pk>\d+)/update$',  login_required(report_update),                    name='update_partial'),
                       url(r'^(?P<pk>\d+)/verify$',  login_required(report_verify),                    name='verify'),
                       url(r'^(?P<pk>\d+)/close$',   login_required(report_close),                     name='close'),
                       url(r'^(?P<pk>\d+)/comment$', login_required(report_comment),                   name='comment'),
                       url(r'^(?P<pk>\d+)/comment/(?P<comment_pk>\d+)/remove$', login_required(report_remove_comment), name='remove_comment'),


                       #url(r'^public/statistics(\.(?P<extension>(json)))?$', statistics_view,         name='public_statistics_'),
                       #url(r'^public/statistics/by-date$', statistics_reports_by_date,         name='public_statistics_reports_by_date'),

                       url(r'^categories/', include('violations_categories.urls', namespace="categories")),
                       url(r'^features/',   include('violations_features.urls', namespace="features")),
                       url(r'^victims/',    include('violations_victims.urls', namespace="victims")),

                       )
