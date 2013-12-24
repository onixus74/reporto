from datetime import datetime, date
import json
import logging
import logging
import os
import shutil
import uuid

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.files.storage import default_storage
from django.db.models import Count, Min, Sum, Max, Avg
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from base.utils.views import JSONResponse, JSONDataView, ListHybridResponseMixin, \
    PaginatedListHybridResponseMixin, DetailHybridResponseMixin, \
    AjaxableResponseMixin

from .models import *


logger = logging.getLogger(__name__)


class ReportCreateForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ('created_by',)


def thank_submit(request, template_name="thanks/submit.html", *args, **kwargs):
    logger.debug('POST %s', request.POST)
    logger.debug('FILES %s', request.FILES)

    links = request.POST.getlist('links[]')
    logger.debug('LINKS %s', links)

    context = {}
    form = ReportCreateForm(request.POST or None, request.FILES or None)
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

        #thank = Report.objects.get(pk=thank.pk)

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


class ReportView(DetailHybridResponseMixin, DetailView):

    """ """
    model = Report
    template_name = "thanks/view.html"


class ReportsDashboard(PaginatedListHybridResponseMixin, ListView):

    """ """
    model = Report
    template_name = "thanks/dashboard.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """ """
        context = super(ReportsDashboard, self).get_context_data(**kwargs)

        if self.is_json():

            reports = context.pop('report_list')
            context['html'] = render_to_string("thanks/dashboard_thanks_list.html", {'report_list': reports})

        else:

            thanks_by_date = Report.objects.extra({'date': "date(datetime)"}).values('date').annotate(Count('id')).order_by('date')
            context['thanks_by_date'] = [{'date': i['date'], 'count': i['id__count']} for i in thanks_by_date]

            context['thanks_locations'] = Report.objects.values('latitude', 'longitude', 'category__definition')

        return context
