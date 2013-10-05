from django.conf.urls import patterns, url, include
from victims.views import *

from base.utils.urls import administrator_required


urlpatterns = patterns('',
	url(r'^(\.(?P<extension>(json)))?$',            administrator_required(VictimListHybridView.as_view()),   name='list'),
	url(r'^new$',                                   administrator_required(VictimCreateView.as_view()),       name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(VictimDetailHybridView.as_view()), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      administrator_required(VictimUpdateView.as_view()),       name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    administrator_required(VictimDeleteView.as_view()),       name='delete'),
)
