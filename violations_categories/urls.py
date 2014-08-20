from django.conf.urls import patterns, url

from base.utils.urls import administrator_required

from .views import *


urlpatterns = patterns('',
    url(r'^(\.(?P<extension>(json)))?$',            administrator_required(CategoryListHybridView.as_view()),   name='list'),
    url(r'^new$',                                   administrator_required(CategoryCreateView.as_view()),       name='create'),
    url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(CategoryDetailHybridView.as_view()), name='view'),
    url(r'^(?P<pk>\d+)/edit$',                      administrator_required(CategoryUpdateView.as_view()),       name='edit'),
    url(r'^(?P<pk>\d+)/delete$',                    administrator_required(CategoryDeleteView.as_view()),       name='delete'),
)
