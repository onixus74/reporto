from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
import json

from django.contrib.auth.decorators import login_required, permission_required

from reports.models import *

from django import forms
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.base import View
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import JSONResponse, JSONDataView, ListHybridResponseMixin, DetailHybridResponseMixin

def index(request, *args, **kwargs):
	template_name = "reports/index.html"
	context = {
		"object_list": Report.objects.all()
	}
	return render_to_response(template_name, context)


def dashboard(request, template_name = "reports/dashboard.html", *args, **kwargs):
	context = {
		"object_list": Report.objects.all()
	}
	return render_to_response(template_name, context)


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report

class ReportXView(FormView):
		template_name = 'reports/new.html'
		form_class = ReportForm
		success_url = '/'

		def form_valid(self, form):
				# This method is called when valid form data has been POSTed.
				# It should return an HttpResponse.
				form.send_email()
				return super(ContactView, self).form_valid(form)


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

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


@csrf_exempt
def submit_upload(request, *args, **kwargs):
	print request.session.items()
	print request.method
	#print request.body
	#print request.META['CONTENT_TYPE']
	print request.COOKIES
	print request.REQUEST
	print request.GET
	print request.POST
	print request.FILES
	return JSONResponse({'done': True})


def stats_xxx(request, *args, **kwargs):
	#data = Report.objects.get() # data request
	response = {
	 #'reports': data,
	 'Verbal Vilence': 15,
	 'Vilance': 10,
	}
	return JSONResponse(response)


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


	def form_valid(self, form):
		form.instance.location_text = form.instance.location
		form.instance.created_by = self.request.user
		return super(ReportSubmitView, self).form_valid(form)


class ReportSubmitPublicView(CreateView):
	model = Report
	template_name = "reports/submit-public.html"


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
