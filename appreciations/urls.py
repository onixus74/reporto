from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from base.utils.urls import login_required_with_message, administrator_required
from appreciations.views import *


urlpatterns = patterns('',
                       # url(r'^(\.(?P<extension>(json)))?$',       administrator_required(ReportsDashboard.as_view()),       name='dashboard'),
                       url(r'^(\.(?P<extension>(json)))?$',       ReportsDashboard.as_view(),       name='dashboard'),
                       url(r'^search(\.(?P<extension>(json)))?$', ReportSearchView.as_view(),       name='search'),
                       url(r'^submit$',            login_required_with_message(appreciation_submit),                    name='submit'),
                       url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$',    ReportView.as_view(),             name='view'),
                       url(r'^(?P<pk>\d+)/partial$',    ReportPartialView.as_view(),             name='view_partial'),
                       url(r'^categories/', include('appreciations_categories.urls', namespace="categories")),
                       )
