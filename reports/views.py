import logging

import uuid
import os
import json
import logging

from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson

from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.base import View
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from base.utils.views import JSONResponse, JSONDataView, ListHybridResponseMixin, DetailHybridResponseMixin

from django.core.files.storage import default_storage

from reports.models import *

logger = logging.getLogger(__name__)


def index(request, template_name = "reports/index.html", *args, **kwargs):
	context = {
		"object_list": Report.objects.all()
	}
	return render_to_response(template_name, context)


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report


class ReportsDashboard(ListHybridResponseMixin, ListView):
	""" """
	model = Report
	template_name = "reports/dashboard.html"

	# def get_context_data(self, **kwargs):
	# 	context = super(PublisherDetail, self).get_context_data(**kwargs)
	# 	context['something'] = Something.objects.all()
	# 	return context

class ReportView(DetailHybridResponseMixin, DetailView):
	""" """
	model = Report
	template_name = "reports/view.html"



# def item(request, id, *args, **kwargs):
# 	template_name = "reports/view.html"
# 	context = {
# 		"object": Report.objects.get(id=id)
# 	}
# 	return render_to_response(template_name, context)


# @csrf_exempt
# class SubmissionForm(forms.Form):
# 	name = forms.CharField('Name', required=True)


# def submission(request, template_name = "reports/submit.html", *args, **kwargs):
# 	form = SubmissionForm(request.POST or None)
# 	#form = SubmissionForm(request.POST or None, request.FILES or None)
# 	if form.is_valid():
# 		print "form valid"
# 		return redirect("home")
# 	context = {
# 		"message": "Hello!",
# 		"form": form
# 	}
# 	return render_to_response(template_name, context)


# def submission_json(request, *args, **kwargs):
# 	data = {
# 		"message": "Hello!",
# 	}
# 	return HttpResponse(simplejson.dumps(data), content_type="application/json")



# class ReportSubmissionForm(forms.Form):
# 	class Meta:
# 		model = Report
# 		#fields = [...]



class ReportCreateForm(forms.ModelForm):
		class Meta:
				model = Report
				#fields = ('x', 'y)
				exclude = ('created_by','location_text')


class ReportSubmitView(CreateView):
	""" """
	model = Report
	form_class = ReportCreateForm
	template_name = "reports/submit.html"

	def get_context_data(self, **kwargs):
		logger.debug(kwargs)
		rsid = uuid.uuid1().hex
		RSIDs = self.request.session.get('RSIDs', [])
		RSIDs.append(rsid)
		self.request.session['RSIDs'] = RSIDs
		kwargs['report_submit_id'] = rsid
		logger.debug(kwargs)
		return kwargs

	def form_valid(self, form):
		form.instance.location_text = form.instance.location
		form.instance.created_by = self.request.user
		logger.debug(self.request.POST)
		return super(ReportSubmitView, self).form_valid(form)


class ReportSubmitPublicView(CreateView):
	template_name = "reports/submit-public.html"



class MediaForm(forms.ModelForm):
	class Meta:
		model = Media

class UploadFileForm(forms.Form):
	file = forms.FileField()


#@csrf_exempt
def submit_upload(request, *args, **kwargs):

	logger.debug(request.session.items())
	#logger.debug(request.method)
	#logger.debug(request.body)
	#logger.debug(request.META['CONTENT_TYPE'])
	#logger.debug(request.COOKIES)
	#logger.debug(request.REQUEST)
	#logger.debug(request.GET)
	#logger.debug(request.POST)
	logger.debug(request.FILES)


	#logger.debug("condition:")
	#logger.debug(request.META.has_key('HTTP_X_RSID'))
	#logger.debug(request.META['HTTP_X_RSID'])
	#logger.debug(request.session.get('RSIDs', None))
	#logger.debug(request.META['HTTP_X_RSID'] in request.session.get('RSIDs', []))

	if request.method == 'POST' and request.META.has_key('HTTP_X_RSID') and request.META['HTTP_X_RSID'] in request.session.get('RSIDs', []):

		report_submit_id = request.META['HTTP_X_RSID']
		logger.debug(report_submit_id)

		media_path = os.path.join('reports', report_submit_id)
		logger.debug(media_path)

		media_files_key = 'report_submit_' + report_submit_id + '_files'
		media_files = request.session.get(media_files_key, [])

		logger.debug(media_files)

		files = request.FILES.getlist('files[]')
		logger.debug(files)

		for f in files:
			logger.debug(f)
			file_path = os.path.join(media_path, f.name)
			logger.debug(file_path)
			media_files.append(file_path)
			default_storage.save(file_path, f)

		logger.debug(media_files)

		request.session[media_files_key] = media_files

		return JSONResponse({'done': True})

	return JSONResponse({'done': False}, status=400)



class ReportVerifyView(View):
	http_method_names = ['get', 'post']

	def get(self, request, pk, *args, **kwargs):
		report = Report.objects.get(pk=pk)
		return JSONResponse({'message': "done", 'verified': report.is_verified})

	def post(self, request, pk, *args, **kwargs):
		report = Report.objects.get(pk=pk)
		report.is_verified = True
		report.save()
		return JSONResponse({'message': "done", 'verified': report.is_verified})


class ReportCloseView(View):
	http_method_names = ['get', 'post']

	def get(self, request, pk, *args, **kwargs):
		report = Report.objects.get(pk=pk)
		return JSONResponse({'message': "done", 'closed': report.is_closed})

	def post(self, request, pk, *args, **kwargs):
		report = Report.objects.get(pk=pk)
		report.is_closed = True
		report.save()
		return JSONResponse({'message': "done", 'closed': report.is_closed})



def stats_xxx(request, *args, **kwargs):
	#data = Report.objects.get() # data request
	response = {
	 #'reports': data,
	 'Verbal Vilence': 15,
	 'Vilance': 10,
	}
	return JSONResponse(response)



class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment








# CRUD

class ReportListView(ListView):
	model = Report
	template_name = "reports/manage/list.html"


class ReportListHybridView(ListHybridResponseMixin, ReportListView):
	pass


class ReportDetailView(DetailView):
	model = Report
	template_name = "reports/manage/view.html"


class ReportDetailHybridView(DetailHybridResponseMixin, ReportDetailView):
	pass


class ReportCreateView(CreateView):
	model = Report
	template_name = "reports/manage/new.html"


class ReportUpdateView(UpdateView):
	model = Report
	template_name = "reports/manage/edit.html"


class ReportDeleteView(DeleteView):
	model = Report
	template_name = "reports/manage/delete.html"
	success_url = '/reports/manage/'

