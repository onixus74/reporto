from django.conf.urls import patterns, url, include
from .views import *

from base.utils.urls import administrator_required

urlpatterns = patterns('',
	url(r'^(\.(?P<extension>(json)))?$',            administrator_required(FeatureListHybridView.as_view()),   name='list'),
	url(r'^new$',                                   administrator_required(FeatureCreateView.as_view()),       name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(FeatureDetailHybridView.as_view()), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      administrator_required(FeatureUpdateView.as_view()),       name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    administrator_required(FeatureDeleteView.as_view()),       name='delete'),
)
