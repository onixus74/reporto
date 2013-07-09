from django.conf.urls import patterns, url
from categories.views import CategoryDetailView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = patterns('',

  #url(r'^$', 'categories.views.list', name='list'),
  url(r'^$', CategoryListView.as_view(), name='list'),

  url(r'new$', CategoryCreateView.as_view(), name='create'),
  url(r'(?P<pk>\d+)$',  CategoryDetailView.as_view(), name='view'),
  url(r'(?P<pk>\d+)/edit$',  CategoryUpdateView.as_view(), name='edit'),
  url(r'(?P<pk>\d+)/delete$',  CategoryDeleteView.as_view(), name='delete'),

)
