from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^list$', 'categories.views.list', name='categories_list'),

)

