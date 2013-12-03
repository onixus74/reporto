import logging
logger = logging.getLogger(__name__)

import uuid
import os
import json
import logging
import shutil
from datetime import datetime, date

from django.conf import settings
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson

from django import forms
from django.forms.models import model_to_dict
from django.db.models import Count, Min, Sum, Max, Avg
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.base import View
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_http_methods

from base.utils.views import JSONResponse, JSONDataView, ListHybridResponseMixin, PaginatedListHybridResponseMixin, DetailHybridResponseMixin, AjaxableResponseMixin

from django.core.files.storage import default_storage

from incidents.models import *


class ThankCreateForm(forms.ModelForm):

    class Meta:
        model = ThankReport
        exclude = ('created_by',)


def thank_submit(request, template_name="thanks/submit.html", *args, **kwargs):
    logger.debug('POST %s', request.POST)
    logger.debug('FILES %s', request.FILES)

    links = request.POST.getlist('links[]')
    logger.debug('LINKS %s', links)

    context = {}
    form = ThankCreateForm(request.POST or None, request.FILES or None)
    context['form'] = form

    if form.is_valid():

        form.instance.created_by = request.user

        thank = form.save()

        files = request.FILES.getlist('files[]')
        logger.debug('FILES %s', files)

        #media_path = os.path.join('reports', str(report.pk))
        #logger.debug('MEDIA PATH %s', media_path)

        logger.debug('OBJECT %s', thank)

        for f in files:
            #logger.debug('FILE %s', f)
            thank.media.create(file=f)
            #file_path = os.path.join(media_path, f.name)
            #logger.debug('FILE PATH %s', file_path)
            #file_path = default_storage.save(file_path, f)
            # report.media.create(url=file_path)

        links = request.POST.getlist('links[]')
        logger.debug('LINKS %s', links)

        for l in links:
            thank.media.create(url=l, file=None)

        thank.save()

        #thank = ThankReport.objects.get(pk=thank.pk)

        # logger.debug('THANK %s', thank)
        # logger.debug('THANK %s', model_to_dict(thank))
        # from base.utils.views import dumps
        # logger.debug('THANK %s', dumps(thank))

        if request.is_ajax():
            return JSONResponse({
                'success': True,
                #'object': thank,
                'url': thank.get_absolute_url(),
                'notification': {'title': "Adding Report", 'body': "Report added."}
            })
        else:
            return redirect(thank.get_absolute_url())

    else:
        if request.is_ajax():
            return JSONResponse({
                'success': False,
                'errors': form.errors,
                'notification': {'title': "Adding Thank", 'body': form.errors.get('__all__', None) or form.errors.as_ul() or "Failed to add a thank"}
            }, status=400)

    return render(request, template_name, context)


class ThankView(DetailHybridResponseMixin, DetailView):

    """ """
    model = ThankReport
    template_name = "thanks/view.html"


class ThankReportsDashboard(PaginatedListHybridResponseMixin, ListView):

    """ """
    model = ThankReport
    template_name = "thanks/dashboard.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """ """
        context = super(ThankReportsDashboard, self).get_context_data(**kwargs)

        if self.is_json():

            reports = context.pop('thankreport_list')
            context['html'] = render_to_string("thanks/dashboard_thanks_list.html", {'thankreport_list': reports})

        else:

            thanks_by_date = ThankReport.objects.extra({'date': "date(datetime)"}).values('date').annotate(Count('id')).order_by('date')
            context['thanks_by_date'] = [{'date': i['date'], 'count': i['id__count']} for i in thanks_by_date]

            context['thanks_locations'] = ThankReport.objects.values('latitude', 'longitude', 'category__definition')

        return context
