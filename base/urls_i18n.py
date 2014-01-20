from django.conf.urls import patterns, url, include
#from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
#from django.views.generic import TemplateView

#from base.utils.urls import administrator_required
from base.views import *
#from violations.views import ReportsDashboard


urlpatterns = patterns('',

                       url(r'^users/',      include('users.urls', namespace="users")),

                       url(r'^violations/',    include('violations.urls',    namespace='violations')),
                       url(r'^appreciations/',    include('appreciations.urls',    namespace='appreciations')),

                       )
