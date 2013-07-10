from django.conf.urls import patterns, url
from features.views import FeatureListView ,FeatureDetailView,FeatureCreateView,FeatureUpdateView,FeatureDeleteView

urlpatterns = patterns('',
	url(r'^$', FeatureListView.as_view(), name='list'),

  url(r'new$', FeatureCreateView.as_view(), name='create'),
  url(r'(?P<pk>\d+)$',  FeatureDetailView.as_view(), name='view'),
  url(r'(?P<pk>\d+)/edit$',  FeatureUpdateView.as_view(), name='edit'),
  url(r'(?P<pk>\d+)/delete$',  FeatureDeleteView.as_view(), name='delete')
	)
