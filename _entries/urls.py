from django.conf.urls import patterns, url
from .views import *

from base.utils.urls import administrator_required

urlpatterns = patterns('',
   url(r'^(\.(?P<extension>(json)))?$',            administrator_required(EntryListHybridView.as_view()),   name='list'),
   url(r'^new$',                                   administrator_required(EntryCreateView.as_view()),       name='create'),
   url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', administrator_required(EntryDetailHybridView.as_view()), name='view'),
   url(r'^(?P<pk>\d+)/edit$',                      administrator_required(EntryUpdateView.as_view()),       name='edit'),
   url(r'^(?P<pk>\d+)/delete$',                    administrator_required(EntryDeleteView.as_view()),       name='delete'),
)
