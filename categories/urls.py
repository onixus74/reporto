from django.conf.urls import patterns, url, include
from categories.views import *


urlpatterns = patterns('',
	url(r'^(\.(?P<extension>(json)))?$',            CategoryListHybridView.as_view(),   name='list'),
	url(r'^new$',                                   CategoryCreateView.as_view(),       name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', CategoryDetailHybridView.as_view(), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      CategoryUpdateView.as_view(),       name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    CategoryDeleteView.as_view(),       name='delete'),
)

