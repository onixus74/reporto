from django.conf.urls import patterns, url, include
from categories.views import *
from categories.api import router

urlpatterns = patterns('',

	#url(r'^$', 'categories.views.list', name='list'),
	url(r'^(\.(?P<extension>(json)))?$',            CategoryListMultiView.as_view(),   name='list'),
	url(r'^new$',                                   CategoryCreateView.as_view(),      name='create'),
	url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', CategoryDetailMultiView.as_view(), name='view'),
	url(r'^(?P<pk>\d+)/edit$',                      CategoryUpdateView.as_view(),      name='edit'),
	url(r'^(?P<pk>\d+)/delete$',                    CategoryDeleteView.as_view(),      name='delete'),

	url(r'^api', include(router.urls)),

)

