from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from base.utils.urls import administrator_required

from thanks.views import *


urlpatterns = patterns('',

                       url(r'^categories/', include('thanks_categories.urls', namespace="categories")),

                       )