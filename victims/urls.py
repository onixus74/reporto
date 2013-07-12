from django.conf.urls import patterns, url
from victims.views import VictimListView , VictimDetailView, VictimCreateView, VictimUpdateView, VictimDeleteView

urlpatterns = patterns('',
  url(r'^$', VictimListView.as_view(), name='list'),
  url(r'new$', VictimCreateView.as_view(), name='create'),
  url(r'(?P<pk>\d+)$',  VictimDetailView.as_view(), name='view'),
  url(r'(?P<pk>\d+)/edit$',  VictimUpdateView.as_view(), name='edit'),
  url(r'(?P<pk>\d+)/delete$',  VictimDeleteView.as_view(), name='delete')
)
