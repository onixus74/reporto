from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from base.utils.urls import administrator_required
from appreciations.views import *


urlpatterns = patterns('',
                       url(r'^(\.(?P<extension>(json)))?$',           login_required(ReportsDashboard.as_view()),       name='dashboard'),
                       url(r'^submit$',              login_required(appreciation_submit),                    name='submit'),
                       url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$',    login_required(ReportView.as_view()),             name='view'),
                       url(r'^(?P<pk>\d+)/partial$',    login_required(ReportPartialView.as_view()),             name='view_partial'),
                       url(r'^categories/', include('appreciations_categories.urls', namespace="categories")),
                       )
