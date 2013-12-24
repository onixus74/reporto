from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, \
  permission_required

from base.utils.urls import administrator_required
from users.views import *


#from base.views import *
urlpatterns = patterns('',

                       url(r'^(\.(?P<extension>(json)))?$',            administrator_required(UserListHybridView.as_view()),   name='list'),
                       url(r'^new$',                                   administrator_required(UserCreateView.as_view()),       name='create'),
                       #url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$', login_required(UserDetailHybridView.as_view()),         name='view'),
                       #url(r'^(?P<pk>\d+)/edit$',                      login_required(UserUpdateView.as_view()),               name='edit'),
                       url(r'^(?P<pk>\d+)/delete$',                    administrator_required(UserDeleteView.as_view()),       name='delete'),

                       url(r'^(\.(?P<extension>(json)))?$',            			login_required(UserListHybridView.as_view()),   name='list'),
                       url(r'^(?P<pk>\d+)(\.(?P<extension>(json)))?$',       login_required(user_view),                      name='view'),
                       #url(r'^(?P<username>\w+)(\.(?P<extension>(json)))?$', login_required(user_view),                      name='view-by-username'),

                       url(r'^profile(\.(?P<extension>(json)))?$',           login_required(user_profile_view),              name='profile'),

                       url(r'^change/password$', login_required(user_change_password_view),        name='change_password'),
                       url(r'^change/role$',     administrator_required(user_change_role_view),    name='change_role'),
                       url(r'^change/groups$',   administrator_required(user_change_groups_view),  name='change_groups'),

                       url(r'^groups$',           administrator_required(groups_view),              name='groups'),
                       )
