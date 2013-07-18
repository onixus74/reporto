from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
import json

from django.contrib.auth.decorators import login_required, permission_required

from reports.models import Report

from django import forms
from django.views.decorators.csrf import csrf_exempt


from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import JSONResponse, ListHybridResponseMixin, DetailHybridResponseMixin

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


class ReportsDashboard(ListHybridResponseMixin, ListView):
	model = Report
	template_name = "reports/dashboard.html"


class ReportView(DetailHybridResponseMixin, DetailView):
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


class ReportSubmitView(CreateView):
	model = Report
	template_name = "reports/submit.html"




class ReportSubmitPublicView(CreateView):
	model = Report
	template_name = "reports/submit-public.html"


class ReportVerifyView(View):
	message = "verified"

	def get(self, request, pk, *args, **kwargs):
		print kwargs
		report = Report.objects.get(pk=pk)
		return JSONResponse({'message': self.message, 'verified': report.is_verified})

	def post(self, request, pk, *args, **kwargs):
		report = Report.objects.get(pk=pk)
		report.is_verified = True
		report.save()
		return JSONResponse({'message': self.message, 'verified': report.is_verified})


class ReportCloseView(View):
	message = "closed"

	def get(self, request, *args, **kwargs):
		return JSONResponse({'message': self.message})

	def post(self, request, *args, **kwargs):
		return JSONResponse({'message': self.message})



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
