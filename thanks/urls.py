from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from base.utils.urls import administrator_required

from thanks.views import *


urlpatterns = patterns('',
    url(r'^(\.(?P<extension>(json)))?$',           login_required(ThankReportsDashboard.as_view()),       name='dashboard'),
    url(r'^submit$',              login_required(thank_submit),                    name='submit'),
    url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$',    login_required(ThankView.as_view()),             name='view'),
    url(r'^categories/', include('thanks_categories.urls', namespace="categories")),
)
