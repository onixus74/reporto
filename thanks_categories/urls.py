from django.conf.urls import patterns, url
from .views import *

from base.utils.urls import administrator_required

urlpatterns = patterns('',
   url(r'^(\.(?P<extension>(json)))?$',            administrator_required(ThankCategoryListHybridView.as_view()),   name='list'),
   url(r'^new$',                                   administrator_required(ThankCategoryCreateView.as_view()),       name='create'),
   url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(ThankCategoryDetailHybridView.as_view()), name='view'),
   url(r'^(?P<pk>\d+)/edit$',                      administrator_required(ThankCategoryUpdateView.as_view()),       name='edit'),
   url(r'^(?P<pk>\d+)/delete$',                    administrator_required(ThankCategoryDeleteView.as_view()),       name='delete'),
)
