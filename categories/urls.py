from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^list$', 'categories.views.list', name='categories_list'),

)

