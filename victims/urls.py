from django.conf.urls import patterns, url, include
from victims.views import *

from base.utils.urls import administrator_required


urlpatterns = patterns('',
	url(r'^(\.(?P<extension>(json)))?$',            VictimListHybridView.as_view(),   name='list'),
	url(r'^new$',                                   VictimCreateView.as_view(),       name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', VictimDetailHybridView.as_view(), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      VictimUpdateView.as_view(),       name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    VictimDeleteView.as_view(),       name='delete'),
)
