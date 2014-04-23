import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _

from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.views.generic import FormView, ListView, DetailView

from base.utils.views import JSONResponse, JSONDataView, PaginatedJSONListView, ListHybridResponseMixin, \
    PaginatedListHybridResponseMixin, DetailHybridResponseMixin, \
    AjaxableResponseMixin

from .models import *


class ReportCreateForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ('created_by',)


def appreciation_submit(request, template_name="appreciations/submit.html", *args, **kwargs):
    logger.debug('POST %s', request.POST)
    logger.debug('FILES %s', request.FILES)

    links = request.POST.getlist('links[]')
    logger.debug('LINKS %s', links)

    context = {}
    form = ReportCreateForm(request.POST or None, request.FILES or None)
    context['form'] = form

    if form.is_valid():

        form.instance.created_by = request.user

        appreciation = form.save()

        files = request.FILES.getlist('files[]')
        logger.debug('FILES %s', files)

        #media_path = os.path.join('reports', str(report.pk))
        #logger.debug('MEDIA PATH %s', media_path)

        logger.debug('OBJECT %s', appreciation)

        for f in files:
            #logger.debug('FILE %s', f)
            appreciation.media.create(file=f)
            #file_path = os.path.join(media_path, f.name)
            #logger.debug('FILE PATH %s', file_path)
            #file_path = default_storage.save(file_path, f)
            # report.media.create(url=file_path)

        links = request.POST.getlist('links[]')
        logger.debug('LINKS %s', links)

        for l in links:
            appreciation.media.create(url=l, file=None)

        appreciation.save()

        #appreciation = Report.objects.get(pk=appreciation.pk)

        # logger.debug('THANK %s', appreciation)
        # logger.debug('THANK %s', model_to_dict(appreciation))
        # from base.utils.views import dumps
        # logger.debug('THANK %s', dumps(appreciation))

        if request.is_ajax():
            return JSONResponse({
                'success': True,
                #'object': appreciation,
                'url': appreciation.get_absolute_url(),
                'notification': {'title': _("Adding Report"), 'body': _("Report added.")}
            })
        else:
            return redirect(appreciation.get_absolute_url())

    else:
        if request.is_ajax():
            return JSONResponse({
                'success': False,
                'errors': form.errors,
                'notification': {'title': _("Adding Report"), 'body': form.errors.get('__all__', None) or form.errors.as_ul() or _("Failed to add a report")}
            }, status=400)

    return render(request, template_name, context)


class ReportView(DetailHybridResponseMixin, DetailView):

    """ """
    model = Report
    template_name = "appreciations/view.html"


class ReportPartialView(DetailHybridResponseMixin, DetailView):

    """ """
    model = Report
    template_name = 'appreciations/view_partial.html'


class ReportSearchView(PaginatedJSONListView):

    """ """
    model = Report
    paginate_by = 5

    def get_queryset(self):
        return watson.filter(Report, self.request.GET.get('q', ''))

    def get_context_data(self, **kwargs):
        context = super(ReportSearchView, self).get_context_data(**kwargs)
        context['html'] = render_to_string('appreciations/dashboard_appreciations_list.html', {'report_list': context['report_list']})
        context.pop('report_list')
        context['q'] = self.request.GET.get('q', '')
        return context


class ReportsDashboard(PaginatedListHybridResponseMixin, ListView):

    """ """
    model = Report
    template_name = "appreciations/dashboard.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """ """
        context = super(ReportsDashboard, self).get_context_data(**kwargs)

        if self.is_json():

            reports = context.pop('report_list')
            context['html'] = render_to_string("appreciations/dashboard_appreciations_list.html", {'report_list': reports})

        else:

            appreciations_by_date = Report.objects.extra({'date': "date(datetime)"}).values('date').annotate(Count('id')).order_by('date')
            context['appreciations_by_date'] = [{'date': i['date'], 'count': i['id__count']} for i in appreciations_by_date]

            context['appreciations_locations'] = Report.objects.values('latitude', 'longitude', 'category__definition_en')

        return context
