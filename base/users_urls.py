from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from base.views import *

urlpatterns = patterns('',
	url(r'^(?P<pk>\d+)$',    login_required(user_view),             name='view'),
)