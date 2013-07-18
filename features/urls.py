from django.conf.urls import patterns, url, include
from features.views import *
from features.api import router

urlpatterns = patterns('',
	url(r'^(\.(?P<extension>(json)))?$',            FeatureListHybridView.as_view(),   name='list'),
	url(r'^new$',                                   FeatureCreateView.as_view(),       name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', FeatureDetailHybridView.as_view(), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      FeatureUpdateView.as_view(),       name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    FeatureDeleteView.as_view(),       name='delete'),
	url(r'^api', include(router.urls)),
)
