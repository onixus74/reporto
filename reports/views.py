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
from base.utils.views import ListMultiResponseMixin, DetailMultiResponseMixin

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


class ReportsDashboard(ListView):
	model = Report
	template_name = "reports/dashboard.html"


@csrf_exempt
class SubmissionForm(forms.Form):
	name = forms.CharField('Name', required=True)


def submission(request, template_name = "reports/submission.html", *args, **kwargs):
	form = SubmissionForm(request.POST or None)
	#form = SubmissionForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print "form valid"
		return redirect("home")
	context = {
		"message": "Hello!",
		"form": form
	}
	return render_to_response(template_name, context)


def submission_json(request, *args, **kwargs):
	data = {
		"message": "Hello!",
	}
	return HttpResponse(simplejson.dumps(data), content_type="application/json")


class ReportSubmissionForm(forms.Form):
	class Meta:
		model = Report
		#fields = [...]


class ReportSubmission(CreateView):
	model = Report
	template_name = "reports/submission.html"


def item(request, id, *args, **kwargs):
	template_name = "reports/view.html"
	context = {
		"object": Report.objects.get(id=id)
	}
	return render_to_response(template_name, context)


# CRUD

class ReportListView(ListView):
	model = Report
	template_name = "reports/list.html"


class ReportListMultiView(ListMultiResponseMixin, ReportListView):
	pass


class ReportDetailView(DetailView):
	model = Report
	template_name = "reports/view.html"


class ReportDetailMultiView(DetailMultiResponseMixin, ReportDetailView):
	pass


class ReportCreateView(CreateView):
	model = Report
	template_name = "reports/new.html"


class ReportUpdateView(UpdateView):
	model = Report
	template_name = "reports/edit.html"


class ReportDeleteView(DeleteView):
	model = Report
	template_name = "reports/delete.html"
	success_url = '/reports/'
